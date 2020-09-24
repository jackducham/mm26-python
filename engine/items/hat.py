from engine.items.status_modifier import StatusModifier
from engine.items.wearable import Wearable
from protos import item_pb2


class Hat(Wearable):
    # TODO add documentation for these
    magic_effect_types = ["LINGERING_POTIONS", "SHOES_BOOST", "CLOTHES_BOOST",
                          "WEAPON_BOOST", "TRIPLED_ON_HIT", "STACKING_BONUS", "NONE"]

    def __init__(self, hat_proto: item_pb2.Hat):
        if not isinstance(hat_proto, item_pb2.Hat):
            raise ValueError('Incorrect object type; expected item_pb2.Hat, got {}'.format(type(hat_proto)))
        super().__init__(StatusModifier(kwargs={'status_modifier_proto': hat_proto.stats}))

        self.magic_effect = hat_proto.magic_effect

    def get_magic_effect(self):
        return self.magic_effect
