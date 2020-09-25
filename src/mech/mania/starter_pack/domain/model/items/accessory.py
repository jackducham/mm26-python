from mech.mania.starter_pack.domain.model.items.status_modifier import StatusModifier
from mech.mania.starter_pack.domain.model.items.wearable import Wearable
from mech.mania.engine.domain.model import item_pb2


class Accessory(Wearable):
    # For details, see https://github.com/jackducham/mm26-design/wiki/Magic-Effects
    magic_effect_types = ["LINGERING_POTIONS", "SHOES_BOOST", "CLOTHES_BOOST",
                          "WEAPON_BOOST", "TRIPLED_ON_HIT", "STACKING_BONUS", "NONE"]

    def __init__(self, accessory_proto: item_pb2.Accessory):
        if not isinstance(accessory_proto, item_pb2.Accessory):
            raise ValueError('Incorrect object type; expected item_pb2.Accessory, got {}'.format(type(accessory_proto)))
        super().__init__(StatusModifier(kwargs={'status_modifier_proto': accessory_proto.stats}))

        self.magic_effect = accessory_proto.magic_effect
        self.turns_to_deletion = accessory_proto.turns_to_deletion

    def get_magic_effect(self):
        return self.magic_effect
