import uuid
from threading import Lock
from typing import Dict, Optional

from flask import Flask, render_template, redirect, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room
from src.game.game import Game, PlayerIsDead
from data import res


class Lobby:
    players: Dict[str, dict]
    owner: dict
    lobby_id: str
    g: Optional[Game]
    mtx: Lock
    game_status: str

    def __init__(self, owner, lobby_id):
        self.owner = owner
        self.lobby_id = lobby_id
        self.players = {}
        self.g = None
        self.mtx = Lock()

    def enter_lobby(self, player):
        if self.g is not None:
            return
        if player["username"] in self.players:
            return
        join_room(self.lobby_id)
        self.players[player["username"]] = player
        emit("lobby players", dict(players=list(self.players.values())), to=self.lobby_id)

    def start(self, starter_name):
        if self.g is None and self.owner["username"] == starter_name:
            names = [p["username"] for p in self.players.values()]
            classes = [p["class"] for p in self.players.values()]
            self.g = Game(names, classes, shape)
            for p in self.players.values():
                emit("update", self.g.player_see(p["username"]), to=p["sid"])  # hopefully it will work
        return self.g

    def remove_player(self, sid):
        with self.mtx:
            for n, p in self.players.items():
                if p["sid"] == sid:
                    del self.players[n]
                    if self.g is not None:
                        self.g.remove_player(n)
                    break
            return len(self.players) == 0

    def update(self, player_name, action):
        with self.mtx:
            print(self.g.active_player_name)
            game_status = self.g.get_status()
            if game_status != "in_progress":
                emit("game over", dict(message="game-long-over", game_status=game_status), to=request.sid)
                return
            if self.g.active_player_name == player_name:
                self.g.run_checks()
                self.g.run_action(action)  # TODO validate action - gatther all possible action and check action
                if self.g.who_action != "игрок":
                    self.g.run_mech()
                self.g.run_checks()
                new_players = {}
                for p in self.players.values():
                    try:
                        emit("update", self.g.player_see(p["username"]), to=p["sid"])
                        new_players[p["username"]] = p
                    except PlayerIsDead:
                        emit("game over", dict(game_status="lose"), to=p["sid"])
                        leave_room(self.lobby_id, p["sid"])
                self.players = new_players

                game_status = self.g.get_status()
                if game_status != "in_progress":
                    emit("game over", dict(message="game-over", game_status=game_status), to=self.lobby_id)
                    close_room(self.lobby_id)


app = Flask(__name__)
socket = SocketIO(app)
shape = (25, 25)
lobbies = dict()


@app.route('/')
def index():
    return render_template('index.html', async_mode=socket.async_mode)


@app.errorhandler(404)
def handle_404(e):
    return redirect("/")


@app.route("/info")
def info():
    return dict(classes=res.classes)


@socket.on("new")
def new_lobby(player):
    print('new lobby')
    print([e.__dict__ for e in lobbies.values()])
    print(player, request.sid)
    # { "username" : "vasya", "class", "рыцарь" }
    lobby_id = str(uuid.uuid4()).replace('-', '')
    player["sid"] = request.sid
    lobby = Lobby(player, lobby_id)
    lobby.enter_lobby(player)
    lobbies[lobby_id] = lobby
    return emit("lobby created", dict(id=lobby_id), to=request.sid)  # hopefully it will work


@socket.on("join")
def join_lobby(player):
    print('join')
    print([e.__dict__ for e in lobbies.values()])
    print(player, request.sid)
    # { "username" : "vasya", "рыцарь", "lobby_id" : "lobby" }
    lobby_id = player.get("lobby_id")
    player["sid"] = request.sid
    if lobby_id in lobbies:
        lobbies[lobby_id].enter_lobby(player)
    else:
        return emit("error", dict(status=404, message="lobby not found"), to=request.sid)


@socket.on("disconnect")
def disconnect():
    global lobbies
    s = request.sid
    new_lobby = dict()
    for i, l in lobbies.items():
        if not l.remove_player(s):
            new_lobby[i] = l
    lobbies = new_lobby


@socket.on("move")
def move(data):
    # { "lobby_id" : "lobby", "username" : "vasya", "action" : ["move_player", "up"] }
    # see src/io/key_input.py for action specifications
    # ["use_main_weapon", "up"]
    lobby_id = data.get("lobby_id")
    if lobby_id in lobbies:
        lobby = lobbies[lobby_id]
        lobby.update(data.get("username"), data.get("action"))


@socket.on("start")
def start(data):
    # { "lobby_id" : "lobby", "username" : "vasya" }
    print('start')
    print([e.__dict__ for e in lobbies.values()])
    print(data, request.sid)
    lobby_id = data.get("lobby_id")
    if lobby_id in lobbies:
        g = lobbies[lobby_id].start(data.get("username"))
        if g is None:
            return emit("error", dict(status=400, message="failed to start game"))
        return emit("game started", to=lobby_id)
    return emit("error", dict(status=404, message="game not found"))


if __name__ == "__main__":
    socket.run(app)
