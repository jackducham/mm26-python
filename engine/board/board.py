from engine.characters.position import Position
from protos import board_pb2


class Board:
    def __init__(self, proto_board: board_pb2.Board):
        if not isinstance(proto_board, board_pb2.Board):
            raise ValueError('Incorrect object type; expected board_pb2.Board, got {}'.format(type(proto_board)))

        rows = proto_board.rows
        cols = proto_board.cols
        self.grid = []

        for x in range(rows):
            row = []
            for y in range(cols):
                row.append(proto_board.grid[x * cols + y])
            self.grid.append(row)

        self.portals = []
        for i in range(len(proto_board.portals)):
            self.portals.append(Position(proto_board.portals[i]))

    def get_grid(self):
        """
        Returns a 2D array of tiles where the tile at (X, Y) is grid[X][Y]
        """
        return self.grid

    def get_portals(self):
        return self.portals
