from protos import character_pb2
from engine.characters import character


class Monster(character.Character):
    def __init__(self, monster_proto: character_pb2.Monster):

        if not isinstance(monster_proto, character_pb2.Character):
            raise ValueError(
                'Incorrect object type; expected character_pb2.Monster, got {}'.format(
                    type(
                        monster_proto
                    )))

        super().__init__(monster_proto.character)

        self.drops = []
