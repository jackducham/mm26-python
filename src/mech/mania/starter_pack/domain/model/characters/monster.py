from mech.mania.engine.domain.model import character_pb2
from mech.mania.starter_pack.domain.model.characters import character


class Monster(character.Character):
    def __init__(self, monster_proto: character_pb2.Monster):

        super().__init__(monster_proto.character)

        self.monster_proto = monster_proto

        self.aggro_range = monster_proto.aggro_range

    def get_aggro_range(self):
        return self.aggro_range

    def build_proto_class(self):
        return self.monster_proto
