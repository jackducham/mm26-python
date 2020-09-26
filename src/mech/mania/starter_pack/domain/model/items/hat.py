from mech.mania.engine.domain.model import item_pb2
from mech.mania.starter_pack.domain.model.items.status_modifier import StatusModifier
from mech.mania.starter_pack.domain.model.items.wearable import Wearable


class Hat(Wearable):
    # For details, see https://github.com/jackducham/mm26-design/wiki/Magic-Effects
    magic_effect_types = ["LINGERING_POTIONS", "SHOES_BOOST", "CLOTHES_BOOST",
                        "WEAPON_BOOST", "TRIPLED_ON_HIT", "STACKING_BONUS"]

    def __init__(self, hat_proto: item_pb2.Hat):
        super().__init__(StatusModifier(kwargs={'status_modifier_proto': hat_proto.stats}))

        self.magic_effect = hat_proto.magic_effect
        self.turns_to_deletion = hat_proto.turns_to_deletion

    def magic_hat_effect(self):
        return self.magic_effect
