import unittest
from models.configuration import (
    configuration, set_config, get_config
)
from server.game_server import GameServer, GameNotFound
import tempfile
import os


class TestGameServer(unittest.TestCase):
    def setUp(self):
        set_config('quarto_game_store', tempfile.mkdtemp())
        self.game_server = GameServer(configuration)

    def test_create_game(self):
        game_uuid, game = self.game_server.create_game('paul')
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    get_config('quarto_game_store'),
                    game_uuid
                )
            )
        )

    def test_get_game_does_not_exist(self):
        with self.assertRaises(GameNotFound):
            self.game_server.load_game('bob')

    def test_get_game_exists(self):
        game_uuid, game = self.game_server.create_game('paul')

        game2 = self.game_server.load_game(game_uuid)
        self.assertEqual(
            game.to_dict(),
            game2.to_dict()
        )

    def test_join_game(self):
        game_uuid, game = self.game_server.create_game('paul')

        game = self.game_server.join_game(game_uuid, 'sam')
        self.assertEqual(
            game.player_b.name, 'sam'
        )

    def test_join_game_full(self):
        game_uuid, game = self.game_server.create_game('paul')

        self.game_server.join_game(game_uuid, 'sam')
        with self.assertRaises(Exception):
            self.game_server.join_game(game_uuid, 'bob')

    def test_join_game_already_joined(self):
        game_uuid, game = self.game_server.create_game('paul')
        with self.assertRaises(Exception):
            self.game_server.join_game(game_uuid, 'paul')
