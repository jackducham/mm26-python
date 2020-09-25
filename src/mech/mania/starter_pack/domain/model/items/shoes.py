from mech.mania.engine.domain.model import item_pb2
from mech.mania.starter_pack.domain.model.items.status_modifier import StatusModifier
from mech.mania.starter_pack.domain.model.items.wearable import Wearable


class Shoes(Wearable):
    def __init__(self, shoes_proto: item_pb2.Shoes):
        super().__init__(StatusModifier(kwargs={'status_modifier_proto': shoes_proto.stats}))
        self.turns_to_deletion = shoes_proto.turns_to_deletion