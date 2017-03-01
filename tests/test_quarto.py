import unittest
from models.quarto import (
    Game, PlacementMove, PickingMove, Player, Event, Piece, Board
)


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


class TestBoard(unittest.TestCase):
    def test_setup(self):
        board = Board()
        self.assertEqual(
            len(board.positions),
            4
        )
        for column in board.positions:
            self.assertEqual(
                len(column),
                4
            )

    def test_setup_specify_size(self):
        board = Board(3)
        self.assertEqual(
            len(board.positions),
            3
        )
        for column in board.positions:
            self.assertEqual(
                len(column),
                3
            )

    def test_get_rows_bottom_left(self):
        board = Board()
        rows = board.get_rows(0, 0)
        self.assertEqual(
            rows,
            [
                [(0, 0), (1, 0), (2, 0), (3, 0)],
                [(0, 0), (0, 1), (0, 2), (0, 3)],
                [(0, 0), (1, 1), (2, 2), (3, 3)]
            ]
        )

    def test_get_rows_mid_right(self):
        board = Board()
        rows = board.get_rows(3, 2)
        self.assertEqual(
            rows,
            [
                [(0, 2), (1, 2), (2, 2), (3, 2)],
                [(3, 0), (3, 1), (3, 2), (3, 3)]
            ]
        )

    def test_get_rows_mid(self):
        board = Board(3)
        rows = board.get_rows(1, 1)
        self.assertEqual(
            rows,
            [
                [(0, 1), (1, 1), (2, 1)],
                [(1, 0), (1, 1), (1, 2)],
                [(0, 0), (1, 1), (2, 2)],
                [(0, 2), (1, 1), (2, 0)]
            ]
        )

    def test_get_simple(self):
        board = Board(2)
        for x in range(2):
            for y in range(2):
                self.assertEqual(
                    board.get(x, y),
                    None
                )

    def test_get_simple_bad(self):
        board = Board(2)
        for x, y in [
            (1, 5), (5, 1), (-1, 2), (3, -2)
        ]:
            with self.assertRaises(Exception):
                board.get(x, y)

    def test_put_simple(self):
        board = Board(2)
        piece = Piece.from_attributes(True, False)
        board.put(piece, 1, 1)
        with self.assertRaises(Exception):
            board.put(piece, 1, 1)


class TestPiece(unittest.TestCase):
    def test_creation(self):
        standard_piece = Piece.from_attributes()
        self.assertEqual(standard_piece.value, 0)

    def test_creation_with_positive_attributes(self):
        standard_piece = Piece.from_attributes(True)
        self.assertEqual(standard_piece.value, 1)

        standard_piece = Piece.from_attributes(True, True)
        self.assertEqual(standard_piece.value, 3)

        standard_piece = Piece.from_attributes(True, True, True, True)
        self.assertEqual(standard_piece.value, 15)

        standard_piece = Piece.from_attributes(True, False, True, True)
        self.assertEqual(standard_piece.value, 13)

        standard_piece = Piece.from_attributes(True, False, False, True)
        self.assertEqual(standard_piece.value, 9)

    def test_piece_overlap_opposite(self):
        standard_piece = Piece.from_attributes()
        opposite_piece = Piece.from_attributes(True, True, True, True)
        self.assertFalse(
            Piece.overlap(
                standard_piece,
                opposite_piece
            )
        )

    def test_piece_overlap(self):
        standard_piece = Piece.from_attributes()
        opposite_piece = Piece.from_attributes(True, True, False, True)
        self.assertTrue(
            Piece.overlap(
                standard_piece,
                opposite_piece
            )
        )

    def test_positive_overlap(self):
        a = Piece.from_attributes(True, True, False, True)
        b = Piece.from_attributes(True, False, False, True)
        c = Piece.from_attributes(True, True, False, False)
        d = Piece.from_attributes(True, False, True, False)
        self.assertTrue(
            Piece.overlap(
                a, b, c, d
            )
        )

    def test_negative_overlap(self):
        a = Piece.from_attributes(True, True, False, True)
        b = Piece.from_attributes(True, False, False, True)
        c = Piece.from_attributes(False, True, False, False)
        d = Piece.from_attributes(True, False, False, False)
        self.assertTrue(
            Piece.overlap(
                a, b, c, d
            )
        )

    def test_no_overlap(self):
        a = Piece.from_attributes(True, True, False, True)
        b = Piece.from_attributes(True, False, True, True)
        c = Piece.from_attributes(False, True, False, False)
        d = Piece.from_attributes(True, False, False, False)
        self.assertFalse(
            Piece.overlap(
                a, b, c, d
            )
        )

    def test_full_overlap(self):
        pieces = []
        for black in (True, False):
            for tall in (True, False):
                for hole in (True, False):
                    for square in (True, False):
                        pieces.append(
                            Piece.from_attributes(black, tall, hole, square)
                        )
        for piece in pieces:
            overlaps = 0
            for other_piece in pieces:
                if piece == other_piece:
                    continue
                if Piece.overlap(piece, other_piece):
                    overlaps += 1

            self.assertEqual(
                overlaps, 14
            )

    def test_to_dict(self):
        self.assertEqual(
            Piece(5).to_dict(),
            {'value': 5}
        )

    def test_from_dict(self):
        self.assertEqual(
            Piece.from_dict(
                {'value': 5}
            ),
            Piece(5)
        )



if __name__ == '__main__':
    unittest.main()
