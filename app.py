from flask import Flask, request, jsonify
from server.game_server import GameServer, GameNotFound
from server.flask_helpers import InvalidUsage
from models.configuration import configuration


app = Flask(__name__)


def set_game_server(game_server):
    app.game_server = game_server


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


@app.route("/")
def hello():
    return "Hello World!"


def _get_required_param(param_name):
    param = request.values.get(param_name)
    if param is None:
        raise InvalidUsage(
            'Missing parameter "{}"'.format(param_name),
            status_code=400
        )
    return param


@app.route("/api/v1/game/quarto", methods=["POST"])
def create_game():
    player_name = _get_required_param('player_name')
    game_uuid, game = app.game_server.create_game(
        player_name
    )
    return jsonify({
        "game_uuid": game_uuid
    })


@app.route("/api/v1/game/quarto/<game_uuid>", methods=["GET"])
def get_game(game_uuid):
    game = app.game_server.load_game(game_uuid)
    return jsonify(
        game.to_dict()
    )


@app.route("/api/v1/game/quarto/<game_uuid>/join", methods=["POST"])
def join_game(game_uuid):
    player_name = _get_required_param('player_name')

    app.game_server.join_game(
        game_uuid,
        player_name
    )
    return 'ok'


@app.route("/api/v1/game/quarto/<game_uuid>/pick", methods=["POST"])
def pick_piece(game_uuid):
    player_name = _get_required_param('player_name')
    number = _get_required_param('number')
    app.game_server.picking_move(game_uuid, player_name, number)
    return 'ok'


@app.route("/api/v1/game/quarto/<game_uuid>/place", methods=["POST"])
def place_piece(game_uuid):
    player_name = _get_required_param('player_name')
    x = _get_required_param('x')
    y = _get_required_param('y')
    app.game_server.placement_move(game_uuid, player_name, x, y)
    return 'ok'


if __name__ == "__main__":
    set_game_server(GameServer(configuration))
    app.run(
        debug=True
    )
