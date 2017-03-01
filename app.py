from flask import Flask, request, jsonify
from server.game_server import GameServer, GameNotFound
from server.flask_helpers import InvalidUsage
from models.configuration import configuration
from models.quarto import GameStateError

from flask_socketio import SocketIO, join_room, leave_room


app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app)


class GameWrapper():
    def __init__(self):
        self.game_server = None
        self.flask_app = None
        self.socket_io = None

    def set_flask_app(self, flask_app):
        self.flask_app = flask_app

    def set_socket_io(self, socket_io):
        self.socket_io = socket_io

    def set_game_server(self, game_server):
        self.game_server = game_server

    def create_game(self, player_name):
        game_uuid, game = self.game_server.create_game(
            player_name
        )
        return game_uuid, game

    def load_game(self, game_uuid):
        return self.game_server.load_game(game_uuid)

    def join_game(self, game_uuid, player_name):
        game = self.game_server.join_game(
            game_uuid,
            player_name
        )
        self.socket_io.server.emit(
            'player_joined', game.player_b.to_dict(), room=game_uuid
        )
        return game

    def pick_piece(self, game_uuid, player_name, number):
        game = self.game_server.picking_move(game_uuid, player_name, number)
        self.socket_io.server.emit(
            'game_event', game.events[-1].to_dict(), room=game_uuid
        )
        if game.winner:
            self.socket_io.server.emit(
                'player_won', game.winner.to_dict(), room=game_uuid
            )
        return game

    def place_piece(self, game_uuid, player_name, x, y):
        game = self.game_server.placement_move(game_uuid, player_name, x, y)
        self.socket_io.server.emit(
            'game_event', game.events[-1].to_dict(), room=game_uuid
        )
        if game.winner:
            self.socket_io.server.emit(
                'player_won', game.winner.to_dict(), room=game_uuid
            )
        return game


game_wrapper = GameWrapper()


def set_game_wrapper(game_wrapper, flask_app):
    flask_app.game_wrapper = game_wrapper


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(GameNotFound)
def handle_game_not_found(error):
    response = jsonify({'message': 'Game not Found'})
    response.status_code = 404
    return response


@app.errorhandler(GameStateError)
def handle_game_state_error(error):
    response = jsonify({'message': error.args[0]})
    response.status_code = 400
    return response


@app.route("/")
def index():
    return app.send_static_file('html/index.html')


def _get_required_param(param_name, typecast=None, data=None):
    if data is None:
        param = request.values.get(param_name)
    else:
        param = data.get(param_name)
    if param is None:
        raise InvalidUsage(
            'Missing parameter "{}"'.format(param_name),
            status_code=400
        )
    try:
        if typecast:
            return typecast(param)
        else:
            return param
    except:
        raise InvalidUsage(
            'Invalid type, expect "{}"'.format(typecast),
            status_code=400
        )


@app.route("/api/v1/game/quarto", methods=["POST"])
def create_game():
    player_name = _get_required_param('player_name')

    game_uuid, game = game_wrapper.create_game(
        player_name
    )
    return jsonify({
        "game_uuid": game_uuid
    })


@app.route("/api/v1/game/quarto/<game_uuid>", methods=["GET"])
def get_game(game_uuid):
    game = game_wrapper.load_game(game_uuid)
    return jsonify(
        game.to_dict()
    )


@app.route("/api/v1/game/quarto/<game_uuid>/join", methods=["POST"])
def join_game(game_uuid):
    player_name = _get_required_param('player_name')
    game = game_wrapper.join_game(game_uuid, player_name)
    return jsonify(
        game.to_dict()
    )


@socketio.on('join_game')
def handle_join_game(json):
    game_uuid = _get_required_param('game_uuid', data=json)
    player_name = _get_required_param('player_name', data=json)
    game_wrapper.join_game(
        game_uuid, player_name
    )


@app.route("/api/v1/game/quarto/<game_uuid>/pick", methods=["POST"])
def pick_piece(game_uuid):
    player_name = _get_required_param('player_name')
    number = _get_required_param('number', int)
    game = game_wrapper.pick_piece(game_uuid, player_name, number)
    return jsonify(
        game.to_dict()
    )


@app.route("/api/v1/game/quarto/<game_uuid>/place", methods=["POST"])
def place_piece(game_uuid):
    player_name = _get_required_param('player_name')
    x = _get_required_param('x', int)
    y = _get_required_param('y', int)
    game = game_wrapper.place_piece(game_uuid, player_name, x, y)
    return jsonify(
        game.to_dict()
    )


@socketio.on('watch_game')
def handle_watch_game(json):
    rooms = socketio.server.rooms(request.sid)
    join_room_uuid = json['game_uuid']
    for room_id in rooms:
        if room_id not in (
            join_room_uuid, request.sid
        ):
            leave_room(room_id)
    join_room(join_room_uuid)
    handle_load_game(json)


@socketio.on('load_game')
def handle_load_game(json):
    game = game_server.load_game(json['game_uuid'])
    socketio.server.emit(
        'game', game.to_dict(), room=request.sid
    )


@socketio.on('place_piece')
def handle_place_piece(json):
    game_uuid = _get_required_param('game_uuid', data=json)
    player_name = _get_required_param('player_name', data=json)
    x = _get_required_param('x', int, data=json)
    y = _get_required_param('y', int, data=json)
    game_wrapper.place_piece(
        game_uuid, player_name, x, y
    )


@socketio.on('pick_piece')
def handle_pick_piece(json):
    game_uuid = _get_required_param('game_uuid', data=json)
    player_name = _get_required_param('player_name', data=json)
    number = _get_required_param('number', int, data=json)
    game_wrapper.pick_piece(
        game_uuid, player_name, number
    )


@socketio.on('join_lobby')
def handle_join_lobby(json):
    name = _get_required_param('name', data=json)


@socketio.on_error()
def error_handler(e):
    print('There was an error', str(e))


if __name__ == "__main__":
    game_server = GameServer(configuration)
    game_wrapper.set_game_server(game_server)
    game_wrapper.set_flask_app(app)
    game_wrapper.set_socket_io(socketio)

    socketio.run(app)
