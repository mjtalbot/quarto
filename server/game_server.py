import os
import json
import uuid
from models.mechanics import Game, Player, PickingMove, PlacementMove, Event
from models.parts import Piece


class GameNotFound(Exception):
    pass


class GameServer:
    def __init__(self, config):
        self.config = config

    def create_game(self, player_name):
        game = Game()
        game.join_game(Player(player_name))
        game_uuid = self._store_game(game)
        return game_uuid, game

    def _store_game(self, game, game_uuid=None):
        if game_uuid is None:
            game_uuid = str(uuid.uuid4())

        storage_path = os.path.join(
            self.config.get('quarto_game_store'),
            game_uuid
        )
        with open(storage_path, 'w') as f:
            f.write(json.dumps(game.to_dict()))
        return game_uuid

    def load_game(self, game_uuid):
        storage_path = os.path.join(
            self.config.get('quarto_game_store'),
            game_uuid
        )
        if not os.path.exists(storage_path):
            raise GameNotFound()
        with open(storage_path, 'r') as f:
            return Game.from_dict(json.loads(f.read()))

    def join_game(self, game_uuid, player_name):
        game = self.load_game(game_uuid)
        player = Player(player_name)
        game.join_game(player)
        self._store_game(game, game_uuid)
        return game

    def picking_move(self, game_uuid, player_name, number):
        game = self.load_game(game_uuid)
        player = Player(player_name)
        piece = Piece(number)
        move = PickingMove(piece)

        self.apply_event(
            game, player, move
        )
        self._store_game(game, game_uuid)
        return game

    def placement_move(self, game_uuid, player_name, x, y):
        game = self.load_game(game_uuid)
        player = Player(player_name)
        move = PlacementMove(x, y)

        self.apply_event(
            game, player, move
        )
        self._store_game(game, game_uuid)
        return game

    def apply_event(self, game, player, move):
        event = Event(player, move)
        game.apply_event(event)
