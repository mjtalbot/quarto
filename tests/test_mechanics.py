import unittest
from models.mechanics import Game, PlacementMove, PickingMove, Player, Event
from models.parts import Piece


class TestGame(unittest.TestCase):
    def test_check_win_no_pieces(self):
        game = Game()
        for x in range(4):
            for y in range(4):
                self.assertEqual(
                    game.check_win(x, y),
                    False
                )

    def test_check_win_vertical(self):
        game = Game()
        a = Piece.from_attributes(True, True, False, True)
        b = Piece.from_attributes(True, False, False, True)
        c = Piece.from_attributes(True, True, False, False)
        d = Piece.from_attributes(True, False, True, False)

        game.board.put(a, 0, 0)
        game.board.put(b, 0, 1)
        game.board.put(c, 0, 2)
        game.board.put(d, 0, 3)
        self.assertEqual(
            game.check_win(0, 0),
            True
        )

    def test_check_win_horizontal(self):
        game = Game()
        a = Piece.from_attributes(True, True, False, True)
        b = Piece.from_attributes(True, False, False, True)
        c = Piece.from_attributes(True, True, False, False)
        d = Piece.from_attributes(True, False, True, False)

        game.board.put(a, 0, 0)
        game.board.put(b, 1, 0)
        game.board.put(c, 2, 0)
        game.board.put(d, 3, 0)
        self.assertEqual(
            game.check_win(0, 0),
            True
        )

    def test_check_no_win_horizontal(self):
        game = Game()
        a = Piece.from_attributes(True, True, False, True)
        b = Piece.from_attributes(True, False, False, True)
        c = Piece.from_attributes(False, True, False, False)
        d = Piece.from_attributes(True, False, True, False)
        game.board.put(a, 0, 0)
        game.board.put(b, 1, 0)
        game.board.put(c, 2, 0)
        game.board.put(d, 3, 0)
        self.assertEqual(
            game.check_win(0, 0),
            False
        )

    def test_check_win_positive_diagonal(self):
        game = Game()

        a = Piece.from_attributes(True, True, False, True)
        b = Piece.from_attributes(True, False, False, True)
        c = Piece.from_attributes(True, True, False, False)
        d = Piece.from_attributes(True, False, True, False)

        game.board.put(a, 0, 0)
        game.board.put(b, 1, 1)
        game.board.put(c, 2, 2)
        game.board.put(d, 3, 3)
        self.assertEqual(
            game.check_win(0, 0),
            True
        )

    def test_check_win_negative_diagonal(self):
        game = Game()
        a = Piece.from_attributes(True, True, False, True)
        b = Piece.from_attributes(True, False, False, True)
        c = Piece.from_attributes(True, True, False, False)
        d = Piece.from_attributes(True, False, True, False)

        game.board.put(a, 0, 3)
        game.board.put(b, 1, 2)
        game.board.put(c, 2, 1)
        game.board.put(d, 3, 0)
        self.assertEqual(
            game.check_win(0, 3),
            True
        )

    def _init_game(self):
        game = Game()
        game.player_a = Player('bob')
        game.player_b = Player('sam')
        return game

    def test_game_bad_move(self):
        game = self._init_game()
        with self.assertRaises(Exception):
            game.apply_event(Event(
                Player('bob'),
                PlacementMove(0, 1)
            ))

    def test_game_bad_player(self):
        game = self._init_game()
        with self.assertRaises(Exception):
            game.apply_event(Event(
                Player('sam'),
                PickingMove(Piece(1))
            ))

    def test_game_good_move(self):
        game = self._init_game()

        game.apply_event(Event(
            Player('bob'),
            PickingMove(Piece(0))
        ))

        self.assertEqual(
            game.turn, 1
        )

        self.assertEqual(
            game.next_piece, Piece(0)
        )

    def test_game_good_placement(self):
        game = self._init_game()

        game.apply_event(Event(
            Player('bob'),
            PickingMove(Piece(0))
        ))

        game.apply_event(Event(
            Player('sam'),
            PlacementMove(0, 0)
        ))

        self.assertEqual(
            game.turn, 2
        )

        self.assertEqual(
            game.next_piece, None
        )

    def test_game_pick_taken(self):
        game = self._init_game()

        game.apply_event(Event(
            Player('bob'),
            PickingMove(Piece(0))
        ))

        game.apply_event(Event(
            Player('sam'),
            PlacementMove(0, 0)
        ))

        with self.assertRaises(Exception):
            game.apply_event(Event(
                Player('sam'),
                PickingMove(Piece(0))
            ))

    def test_game_2nd_pick_good(self):
        game = self._init_game()

        game.apply_event(Event(
            Player('bob'),
            PickingMove(Piece(0))
        ))

        game.apply_event(Event(
            Player('sam'),
            PlacementMove(0, 0)
        ))

        game.apply_event(Event(
            Player('sam'),
            PickingMove(Piece(1))
        ))

        self.assertEqual(
            game.turn, 3
        )

        self.assertEqual(
            game.next_piece.value, 1
        )

    def test_game_2nd_move_taken(self):
        game = self._init_game()

        game.apply_event(Event(
            Player('bob'),
            PickingMove(Piece(0))
        ))

        game.apply_event(Event(
            Player('sam'),
            PlacementMove(0, 0)
        ))

        game.apply_event(Event(
            Player('sam'),
            PickingMove(Piece(1))
        ))

        with self.assertRaises(Exception):
            game.apply_event(Event(
                Player('bob'),
                PlacementMove(0, 0)
            ))

    def test_game_2nd_move_good(self):
        game = self._init_game()

        game.apply_event(Event(
            Player('bob'),
            PickingMove(Piece(0))
        ))

        game.apply_event(Event(
            Player('sam'),
            PlacementMove(0, 0)
        ))

        game.apply_event(Event(
            Player('sam'),
            PickingMove(Piece(1))
        ))

        game.apply_event(Event(
            Player('bob'),
            PlacementMove(0, 1)
        ))

        self.assertEqual(
            game.turn, 4
        )

        self.assertEqual(
            game.next_piece, None
        )

    def test_game_victory_for_bob(self):
        game = self._init_game()

        game.apply_event(Event(
            Player('bob'), PickingMove(Piece(0))
        ))

        game.apply_event(Event(
            Player('sam'), PlacementMove(0, 0)
        ))

        game.apply_event(Event(
            Player('sam'), PickingMove(Piece(1))
        ))

        game.apply_event(Event(
            Player('bob'), PlacementMove(0, 1)
        ))

        game.apply_event(Event(
            Player('bob'), PickingMove(Piece(2))
        ))

        game.apply_event(Event(
            Player('sam'), PlacementMove(0, 2)
        ))

        game.apply_event(Event(
            Player('sam'), PickingMove(Piece(3))
        ))

        self.assertEqual(game.winner, None)
        game.apply_event(Event(
            Player('bob'), PlacementMove(0, 3)
        ))
        self.assertEqual(game.winner, Player('bob'))
        with self.assertRaises(Exception):
            game.apply_event(Event(
                Player('bob'), PickingMove(Piece(4))
            ))


class TestPlacementMove(unittest.TestCase):
    def test_to_dict(self):
        self.assertEqual(
            PlacementMove(1, 2).to_dict(),
            {
                'type': 'PlacementMove',
                'x': 1,
                'y': 2
            }
        )

    def test_from_dict(self):
        placement_move = PlacementMove.from_dict(
            {
                'x': 1, 'y': 2, 'type': 'PlacementMove'
            }
        )
        self.assertEqual(
            placement_move.x,
            1
        )
        self.assertEqual(
            placement_move.y,
            2
        )


class TestPickingMove(unittest.TestCase):
    def test_to_dict(self):
        self.assertEqual(
            PickingMove(Piece(4)).to_dict(),
            {
                'type': 'PickingMove',
                'piece': {
                    'value': 4
                }
            }
        )

    def test_from_dict(self):
        picking_move = PickingMove.from_dict({
            'type': 'PickingMove',
            'piece': {
                'value': 5
            }
        })

        self.assertEqual(
            picking_move.piece.value,
            5
        )


class TestPlayer(unittest.TestCase):
    def test_to_dict(self):
        self.assertEqual(
            Player('sam').to_dict(),
            {'name': 'sam'}
        )

    def test_from_dict(self):
        self.assertEqual(
            Player.from_dict({'name': 'sam'}),
            Player('sam')
        )

    def test_from_dict_crappy(self):
        self.assertNotEqual(
            Player.from_dict({'name': 'sam'}),
            Player('same')
        )


class TestEvent(unittest.TestCase):
    def test_to_dict(self):
        self.assertEqual(
            Event(
                Player('bob'),
                PickingMove(
                    Piece(2)
                )
            ).to_dict(),
            {
                'player': {
                    'name': 'bob'
                },
                'move': {
                    'type': 'PickingMove',
                    'piece': {
                        'value': 2
                    }
                }
            }
        )

    def test_from_dict(self):
        event = Event.from_dict({
            'player': {
                'name': 'bob'
            },
            'move': {
                'type': 'PickingMove',
                'piece': {
                    'value': 2
                }
            }
        })

        self.assertEqual(
            event.player.name, 'bob'
        )
        self.assertIsInstance(
            event.move, PickingMove
        )
        self.assertEqual(
            event.move.piece.value, 2
        )

    def test_placement_move(self):
        event_dict = {
            'player': {
                'name': 'bob'
            },
            'move': {
                'type': 'PlacementMove',
                'x': 5,
                'y': 1
            }
        }
        event = Event.from_dict(event_dict)

        self.assertEqual(
            event.player.name, 'bob'
        )
        self.assertIsInstance(
            event.move, PlacementMove
        )
        self.assertEqual(
            event.move.x, 5
        )
        self.assertEqual(
            event.move.y, 1
        )

        self.assertEqual(event.to_dict(), event_dict)


if __name__ == '__main__':
    unittest.main()
