import random
import uuid
from threading import Lock
from typing import Dict, Optional

from flask import Flask, render_template, redirect, request, send_from_directory
from flask_socketio import SocketIO, emit, join_room, close_room, leave_room
from src.game.game import Game
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
        if player["username"] in self.players:
            emit("error", dict(message="игрок с таким именем уже есть", errtype="duplicate_username"), to=request.sid)
            return
        join_room(self.lobby_id)
        self.players[player["username"]] = player
        emit("join success", to=request.sid)

        with self.mtx:
            if self.g is not None and not self.g.game_over():
                self.g.add_player(player["username"], player["class"])
                emit("game started", to=player["sid"])
                self.update()
            elif self.g is not None:
                game_status = self.g.get_status()
                emit("lobby players", dict(players=list(self.players.values())), to=player["sid"])
                emit("game over", dict(message="game-long-over", game_status=game_status), to=player["sid"])
            else:
                emit("lobby players", dict(players=list(self.players.values())), to=self.lobby_id)

    def start(self, starter_name):
        with self.mtx:
            if self.g is None or self.g.game_over():
                names = [p["username"] for p in self.players.values()]
                classes = [p["class"] for p in self.players.values()]
                self.g = Game(names, classes, shape)
                self.update()
        return self.g

    def remove_player(self, sid):
        with self.mtx:
            for n, p in self.players.items():
                if p["sid"] == sid:
                    del self.players[n]
                    if self.g is not None:
                        self.g.remove_player(n)
                        leave_room(self.lobby_id, sid)
                        self.update()
                    break
            if len(self.players) == 0:
                close_room(self.lobby_id)

    def empty(self):
        return len(self.players) == 0

    def update(self):
        new_players = {}
        for p in self.players.values():
            emit("update", self.g.player_see(p["username"]), to=p["sid"])
            new_players[p["username"]] = p
        self.players = new_players

    def run_action(self, player_name, action):
        if action[0] not in res.player_possible_keys_web:
            print("Незаконное действие:", player_name, action, "разрешены действия", res.player_possible_keys_web)
            return
        with self.mtx:
            game_status = self.g.get_status()
            if game_status != "in_progress":
                emit("game over", dict(message="game-long-over", game_status=game_status), to=request.sid)
                return
            if self.g.active_player_name == player_name:
                self.g.run_action(action)  # TODO validate action - gatther all possible action and check action
                if self.g.who_action != "игрок":
                    self.g.run_mech()
                self.g.run_checks()
                self.update()

                game_status = self.g.get_status()
                if game_status != "in_progress":
                    emit("game over", dict(message="game-over", game_status=game_status), to=self.lobby_id)


app = Flask(__name__)
socket = SocketIO(app, cors_allowed_origins="*")
shape = (250, 250)
lobbies = dict()


@app.route('/')
def index():
    return render_template('index.html', async_mode=socket.async_mode)


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.errorhandler(404)
def handle_404(e):
    return redirect("/")


@app.route("/static_info")
def info():
    return dict(classes=res.classes, names=res.names, random_name=random.choice(res.names))


@socket.on("new room")
def new_lobby(player):
    print('new lobby')
    print([e.__dict__ for e in lobbies.values()])
    print(player, request.sid)
    # { "username" : "vasya", "class", "рыцарь" }
    lobby_id = str(uuid.uuid4()).replace('-', '')[:6]
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
        return emit("error", dict(status=404, message="комната не найдена", errtype="room_not_found"), to=request.sid)


@socket.on("disconnect")
@socket.on("disconnect from room")
def disconnect():
    global lobbies
    s = request.sid
    new_lobby = dict()
    for i, l in lobbies.items():
        l.remove_player(s)
        if not l.empty():
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
        lobby.run_action(data.get("username"), data.get("action"))


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
            emit("error", dict(status=500, message="не удалось начать игру", errtype="game_not_started"), to=request.sid)
        return emit("game started", to=lobby_id)
    return emit("error", dict(status=404, message="комната не найдена", errtype="room_not_found"), to=request.sid)


if __name__ == "__main__":
    socket.run(app)
