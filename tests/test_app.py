import unittest
from models.configuration import (
    configuration, set_config, get_config
)
from server.game_server import GameServer, GameNotFound
import tempfile
import os
import json
from app import app, set_game_server


class TestGameServer(unittest.TestCase):
    def setUp(self):
        set_config('quarto_game_store', tempfile.mkdtemp())
        game_server = GameServer(configuration)
        set_game_server(game_server)
        self.app = app.test_client()

    def test_hello_world(self):
        rv = self.app.get('/')
        self.assertEqual(b'Hello World!', rv.data)

    def _get_game(self, game_uuid):
        rv = self.app.get(
            '/api/v1/game/quarto/{}'.format(game_uuid)
        )

        self.assertEqual(
            rv.status_code,
            200
        )
        return json.loads(rv.data)

    def _create_game(self, player_name):
        rv = self.app.post(
            '/api/v1/game/quarto',
            data=dict(
                player_name=player_name
            )
        )
        self.assertEqual(
            rv.status_code,
            200
        )
        return json.loads(rv.data)

    def _join_game(self, game_uuid, player_name):
        rv = self.app.post(
            '/api/v1/game/quarto/{}/join'.format(game_uuid),
            data=dict(
                player_name=player_name
            )
        )
        self.assertEqual(
            rv.status_code,
            200
        )

    def test_create_game(self):
        json_data = self._create_game('bingo')
        self.assertIn('game_uuid', json_data)

        self.assertTrue(
            os.path.exists(
                os.path.join(
                    get_config('quarto_game_store'),
                    json_data['game_uuid']
                )
            )
        )

    def test_get_game_does_not_exist(self):
        rv = self.app.get(
            '/api/v1/game/quarto/random_game_uuid'
        )
        self.assertEqual(
            rv.status_code,
            404
        )

    def test_get_game_exists(self):
        json_data = self._create_game('bingo')
        game_data = self._get_game(json_data['game_uuid'])
        self.assertEqual(
            game_data['player_a'],
            {'name': 'bingo'}
        )

    def test_join_game(self):
        json_data = self._create_game('bingo')
        game_uuid = json_data['game_uuid']

        rv = self.app.post(
            '/api/v1/game/quarto/{}/join'.format(game_uuid),
            data=dict(
                player_name='sam'
            )
        )
        self.assertEqual(
            rv.status_code,
            200
        )

        game_data = self._get_game(json_data['game_uuid'])

        self.assertEqual(
            game_data['player_b'],
            {'name': 'sam'}
        )

    def test_join_game_full(self):
        json_data = self._create_game('bingo')
        game_uuid = json_data['game_uuid']

        self.app.post(
            '/api/v1/game/quarto/{}/join'.format(game_uuid),
            data=dict(
                player_name='sam'
            )
        )
        rv = self.app.post(
            '/api/v1/game/quarto/{}/join'.format(game_uuid),
            data=dict(
                player_name='sam2'
            )
        )
        self.assertEqual(
            rv.status_code,
            400
        )

    def test_join_game_already_joined(self):
        json_data = self._create_game('bingo')
        game_uuid = json_data['game_uuid']

        rv = self.app.post(
            '/api/v1/game/quarto/{}/join'.format(game_uuid),
            data=dict(
                player_name='bingo'
            )
        )
        self.assertEqual(
            rv.status_code,
            400
        )

    def test_pick_piece_ok(self):
        json_data = self._create_game('bingo')
        self._join_game(json_data['game_uuid'], 'sam')

        rv = self.app.post(
            '/api/v1/game/quarto/{}/pick'.format(
                json_data['game_uuid']
            ),
            data=dict(
                player_name='bingo',
                number=12,
            )
        )
        self.assertEqual(rv.data, b'ok')
