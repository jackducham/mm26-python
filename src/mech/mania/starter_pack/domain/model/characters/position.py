import sys

from mech.mania.engine.domain.model import character_pb2


class Position:
    def __init__(self, position_proto: character_pb2.Position = None):
        self.x = position_proto.x
        self.y = position_proto.y
        self.board_id = position_proto.board_id

    @classmethod
    def create(cls, x, y, board_id):
        temp = character_pb2.Position()
        temp.x = x
        temp.y = y
        temp.board_id = board_id
        return cls(temp)

    def build_from_proto(self, position_proto: character_pb2.Position):
        self.x = position_proto.x
        self.y = position_proto.y
        self.board_id = position_proto.board_id

    def build_proto_class(self):
        position_builder = character_pb2.Position()
        position_builder.x = self.x
        position_builder.y = self.y
        position_builder.board_id = self.board_id

        return position_builder

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_board_id(self):
        return self.board_id

    def __eq__(self, other):
        if other == self:
            return True

        if other is None or type(self) != type(other):
            return False

        return self.x == other.x and self.y == other.y and self.board_id == other.board_id

    def __hash__(self):
        return hash(self)

    def manhattan_distance(self, other):
        if other.board_id != self.board_id:
            return sys.maxsize
        return abs(self.x - other.x) + abs(self.y - other.y)
