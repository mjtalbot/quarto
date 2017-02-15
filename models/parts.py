class Board:
    def __init__(self, size=4):
        self.positions = []
        self.size = size
        for x in range(size):
            self.positions.append([])
            for y in range(size):
                self.positions[x].append(None)

    def put(self, piece, x, y):
        if (
            x < 0 or
            x >= self.size or
            y < 0 or
            y >= self.size
        ):
            raise Exception('Placing outside board')
        if self.positions[x][y] is not None:
            raise Exception('Position already taken')
        self.positions[x][y] = piece

    def get(self, x, y):
        if (
            x < 0 or
            x >= self.size or
            y < 0 or
            y >= self.size
        ):
            raise Exception('Outside board')
        return self.positions[x][y]

    def get_rows(self, x, y):
        # based on x, y return the possible "streaks"
        output_list = []
        output_list.append([
            (_x, y) for _x in range(self.size)
        ])
        output_list.append([
            (x, _y) for _y in range(self.size)
        ])
        if x == y:
            output_list.append([
                (xy, xy) for xy in range(self.size)
            ])
        if x == self.size - (y + 1):
            output_list.append([
                (xy, self.size - (xy + 1)) for xy in range(self.size)
            ])
        return output_list


class Piece:
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_attributes(cls, *attributes):
        total = 0
        value = 1
        for attribute in attributes:
            if attribute is True:
                total += value
            value = value << 1
        return cls(total)

    def to_dict(self):
        return {
            'value': self.value
        }

    @classmethod
    def from_dict(cls, in_dict):
        return cls(in_dict['value'])

    def __eq__(self, other):
        return self.value == other.value

    @classmethod
    def overlap(cls, *pieces, length=4):
        # positive check
        output = pow(2, length)-1
        for piece in pieces:
            output = output & piece.value
        if output > 0:
            return True

        # negative check
        output = pow(2, length)-1
        _max = pow(2, length)-1
        for piece in pieces:
            output = output & (_max - piece.value)
        if output > 0:
            return True
        return False
