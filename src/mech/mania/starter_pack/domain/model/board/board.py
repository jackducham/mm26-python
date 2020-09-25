from mech.mania.engine.domain.model import board_pb2
from mech.mania.starter_pack.domain.model.characters.position import Position


class Board:
    def __init__(self, proto_board: board_pb2.Board):

        rows = proto_board.rows
        cols = proto_board.columns
        self.grid = []

        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(proto_board.grid[r * c + c])
            self.grid.append(row)

        self.portals = []
        for i in range(len(proto_board.portals)):
            # TODO: implement Position
            self.portals.append(Position(proto_board.portals[i]))

    def get_grid(self):
        return self.grid

    def get_portals(self):
        return self.portals
