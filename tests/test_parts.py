import unittest
from models.parts import Board, Piece


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


if __name__ == '__main__':
    unittest.main()
