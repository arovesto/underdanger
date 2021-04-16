import uuid
from threading import Lock

from flask import Flask, render_template, redirect, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room
from src.game.game import Game
from data import res


class Lobby:
    players = dict()
    owner = dict()
    id = ""
    g = None
    mtx = Lock()

    def __init__(self, owner, id_):
        self.owner = owner
        self.id = id_

    def join(self, player):
        if player["username"] in self.players:
            return
        join_room(self.id)
        if len(self.players) > 0:
            emit("current players", dict(players=list(self.players.values())), to=request.sid)
        self.players[player["username"]] = player
        emit("new player", player, to=self.id)

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
            return len(self.players) == 0

    def update(self, player_name, action):
        with self.mtx:  # mutex so no data races like "move while move"
            if self.g.name_act_player == player_name:
                if self.g.who_action != "игрок":  # TODO call this once, idk - doing same thing that in regular game
                    self.g.run_checks()
                    self.g.run_mech()

                self.g.run_checks()
                self.g.run_action(action)  # TODO validate action - gatther all possible action and check action
                if self.g.game_over():
                    emit("game over", dict(message="game-over"), to=self.id)  # TODO win vs fail (see end_of_game)
                    close_room(self.id)
                else:
                    if self.g.who_action != "игрок":
                        self.g.run_checks()
                        self.g.run_mech()
                    for p in self.players.values():
                        emit("update", self.g.player_see(p["username"]), to=p["sid"])  # hopefully it will work


app = Flask(__name__)
socket = SocketIO(app)
shape = (250, 250)
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
    # { "username" : "vasya", "class", "рыцарь" }
    lobby_id = str(uuid.uuid4())
    player["sid"] = request.sid
    lobby = Lobby(player, lobby_id)
    lobby.join(player)
    lobbies[lobby_id] = lobby
    return emit("lobby created", dict(id=lobby_id), to=request.sid)  # hopefully it will work


@socket.on("join")
def join_lobby(player):
    # { "username" : "vasya", "рыцарь", "lobby_id" : "lobby" }
    lobby_id = player.get("lobby_id")
    player["sid"] = request.sid
    if lobby_id in lobbies:
        lobbies[lobby_id].join(player)
        return
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
    lobby_id = data.get("lobby_id")
    if lobby_id in lobbies:
        lobby = lobbies[lobby_id]
        lobby.update(data.get("username"), data.get("action"))


@socket.on("start")
def start(data):
    # { "lobby_id" : "lobby", "username" : "vasya" }
    lobby_id = data.get("lobby_id")
    if lobby_id in lobbies:
        g = lobbies[lobby_id].start(data.get("username"))
        if g is None:
            return emit("error", dict(status=400, message="failed to start game"))
        return emit("game started", to=lobby_id)
    return emit("error", dict(status=404, message="game not found"))


if __name__ == "__main__":
    socket.run(app)
