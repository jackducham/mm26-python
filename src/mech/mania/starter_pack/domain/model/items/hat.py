from mech.mania.engine.domain.model import item_pb2
from mech.mania.starter_pack.domain.model.items.status_modifier import StatusModifier
from mech.mania.starter_pack.domain.model.items.wearable import Wearable


class Hat(Wearable):
    # TODO add documentation for these
    hat_effect_types = ["LINGERING_POTIONS", "SHOES_BOOST", "CLOTHES_BOOST",
                        "WEAPON_BOOST", "TRIPLED_ON_HIT", "STACKING_BONUS"]

    def __init__(self, hat_proto: item_pb2.Hat):
        super().__init__(StatusModifier(kwargs={'status_modifier_proto': hat_proto.stats}))

        self.hat_effect = hat_proto.hat_effect

    def get_hat_effect(self):
        return self.hat_effect
