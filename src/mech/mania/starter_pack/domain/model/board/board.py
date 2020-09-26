from mech.mania.engine.domain.model import board_pb2
from mech.mania.starter_pack.domain.model.characters.position import Position


class Board:
    def __init__(self, proto_board: board_pb2.Board):

        self.proto_board = proto_board

        self.width = proto_board.width
        self.height = proto_board.height
        self.grid = []

        for x in range(self.width):
            row = []
            for y in range(self.height):
                row.append(proto_board.grid[x * self.height + y])
            self.grid.append(row)

        self.portals = []
        for i in range(len(proto_board.portals)):
            self.portals.append(Position(proto_board.portals[i]))

    def get_grid(self):
        """
        Returns a 2D array of tiles where the tile at (X, Y) is grid[X][Y]
        """
        return self.grid

    def get_tile_at(self, pos):
        return self.grid[pos.x][pos.y]

    def get_portals(self):
        return self.portals

    def build_proto_class(self):
        return self.proto_board
