from mech.mania.engine.domain.model import item_pb2
from mech.mania.starter_pack.domain.model.items.status_modifier import StatusModifier


class TempStatusModifier(StatusModifier):
    def __init__(self, temp_status_modifier_proto: item_pb2.TempStatusModifier):
        super().__init__(
            kwargs={'status_modifier_proto': temp_status_modifier_proto.stats}
        )

        self.turns_left = temp_status_modifier_proto.turns_left
        self.damage_per_turn = temp_status_modifier_proto.flat_damage_per_turn

    def get_turns_left(self):
        return self.turns_left

    def get_damage_per_turn(self):
        return self.damage_per_turn
