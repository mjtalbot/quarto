import unittest
from models.mechanics import Game
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


if __name__ == '__main__':
    unittest.main()
