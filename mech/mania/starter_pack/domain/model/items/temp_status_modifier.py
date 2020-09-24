from engine.items.status_modifier import StatusModifier
from protos import item_pb2


class TempStatusModifier(StatusModifier):
    def __init__(self, temp_status_modifier_proto: item_pb2.TempStatusModifier):
        if not isinstance(temp_status_modifier_proto, item_pb2.TempStatusModifier):
            raise ValueError(
                'Incorrect object type; expected item_pb2.TempStatusModifier, got {}'.format(
                    type(
                        temp_status_modifier_proto
                    )))
        super().__init__(
            kwargs={'flat_speed_change': temp_status_modifier_proto.flat_speed_change,
                    'percent_speed_change': temp_status_modifier_proto.percent_speed_change,
                    'flat_health_change': temp_status_modifier_proto.flat_health_change,
                    'percent_health_change': temp_status_modifier_proto.percent_health_change,
                    'flat_experience_change': temp_status_modifier_proto.flat_experience_change,
                    'percent_experience_change': temp_status_modifier_proto.percent_experience_change,
                    'flat_attack_change': temp_status_modifier_proto.flat_attack_change,
                    'percent_attack_change': temp_status_modifier_proto.percent_attack_change,
                    'flat_defense_change': temp_status_modifier_proto.flat_defense_change,
                    'percent_defense_change': temp_status_modifier_proto.percent_defense_change,
                    'flat_regen_per_turn': temp_status_modifier_proto.flat_regen_per_turn}
        )

        self.turns_left = temp_status_modifier_proto.turns_left
        self.damage_per_turn = temp_status_modifier_proto.flat_damage_per_turn

    def get_turns_left(self):
        return self.turns_left

    def get_damage_per_turn(self):
        return self.damage_per_turn
