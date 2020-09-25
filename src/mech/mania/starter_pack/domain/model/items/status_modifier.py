from mech.mania.engine.domain.model import item_pb2


class StatusModifier:
    def __init__(self, **kwargs):
        if 'kwargs' in kwargs.keys():
            kwargs = kwargs['kwargs']
        if 'status_modifier_proto' in kwargs.keys():
            status_modifier_proto = kwargs['status_modifier_proto']

            self.flat_regen_per_turn = status_modifier_proto.flat_regen_per_turn
            self.flat_speed_change = status_modifier_proto.flat_speed_change
            self.flat_health_change = status_modifier_proto.flat_health_change
            self.flat_experience_change = status_modifier_proto.flat_experience_change

            self.flat_attack_change = status_modifier_proto.flat_attack_change
            self.flat_defense_change = status_modifier_proto.flat_defense_change

            self.percent_speed_change = status_modifier_proto.percent_speed_change
            self.percent_health_change = status_modifier_proto.percent_health_change
            self.percent_experience_change = status_modifier_proto.percent_experience_change

            self.percent_attack_change = status_modifier_proto.percent_attack_change
            self.percent_defense_change = status_modifier_proto.percent_defense_change

        else:
            self.flat_regen_per_turn = kwargs['flat_regen_per_turn']
            self.flat_speed_change = kwargs['flat_speed_change']
            self.flat_health_change = kwargs['flat_health_change']
            self.flat_experience_change = kwargs['flat_experience_change']

            self.flat_attack_change = kwargs['flat_attack_change']
            self.flat_defense_change = kwargs['flat_defense_change']

            self.percent_speed_change = kwargs['percent_speed_change']
            self.percent_health_change = kwargs['percent_health_change']
            self.percent_experience_change = kwargs['percent_experience_change']

            self.percent_attack_change = kwargs['percent_attack_change']
            self.percent_defense_change = kwargs['percent_defense_change']

    def get_flat_speed_change(self):
        return self.flat_speed_change

    def get_percent_speed_change(self):
        return self.percent_speed_change

    def get_flat_health_change(self):
        return self.flat_health_change

    def get_percent_health_change(self):
        return self.percent_health_change

    def get_flat_experience_change(self):
        return self.flat_experience_change

    def get_percent_experience_change(self):
        return self.percent_experience_change

    def get_flat_attack_change(self):
        return self.flat_attack_change

    def get_percent_attack_change(self):
        return self.percent_attack_change

    def get_flat_defense_change(self):
        return self.flat_defense_change

    def get_percent_defense_change(self):
        return self.percent_defense_change

    def get_flat_regen_per_turn(self):
        return self.flat_regen_per_turn
