from mech.mania.engine.domain.model import item_pb2
from mech.mania.starter_pack.domain.model.items.status_modifier import StatusModifier
from mech.mania.starter_pack.domain.model.items.temp_status_modifier import TempStatusModifier
from mech.mania.starter_pack.domain.model.items.wearable import Wearable


class Weapon(Wearable):
    def __init__(self, weapon_proto: item_pb2.Weapon):

        super().__init__(StatusModifier(kwargs={'status_modifier_proto': weapon_proto.stats}))
        self.range = weapon_proto.range
        self.splash_radius = weapon_proto.splash_radius
        self.on_hit_effect = TempStatusModifier(weapon_proto.on_hit_effect)
        self.attack = weapon_proto.attack
        self.turns_to_deletion = weapon_proto.turns_to_deletion

    def get_range(self):
        return self.range

    def get_splash_radius(self):
        return self.splash_radius

    def get_on_hit_effect(self):
        return self.on_hit_effect

    def get_attack(self):
        return self.attack
