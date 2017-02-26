from flask import Flask, request, jsonify
from server.game_server import GameServer, GameNotFound
from server.flask_helpers import InvalidUsage
from models.configuration import configuration
from models.mechanics import GameStateError


app = Flask(__name__, static_url_path='/static')


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


@app.errorhandler(GameStateError)
def handle_game_state_error(error):
    response = jsonify({'message': error.args[0]})
    response.status_code = 400
    return response


@app.route("/")
def hello():
    return app.send_static_file('html/index.html')


def _get_required_param(param_name, typecast=None):
    param = request.values.get(param_name)
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
    return jsonify({
        'message': 'ok'
    })


@app.route("/api/v1/game/quarto/<game_uuid>/pick", methods=["POST"])
def pick_piece(game_uuid):
    player_name = _get_required_param('player_name')
    number = _get_required_param('number', int)
    app.game_server.picking_move(game_uuid, player_name, number)
    return jsonify({
        'message': 'ok'
    })


@app.route("/api/v1/game/quarto/<game_uuid>/place", methods=["POST"])
def place_piece(game_uuid):
    player_name = _get_required_param('player_name')
    x = _get_required_param('x', int)
    y = _get_required_param('y', int)
    app.game_server.placement_move(game_uuid, player_name, x, y)
    return jsonify({
        'message': 'ok'
    })


if __name__ == "__main__":
    set_game_server(GameServer(configuration))
    app.run(
        debug=True
    )
