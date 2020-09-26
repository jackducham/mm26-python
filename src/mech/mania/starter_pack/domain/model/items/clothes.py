from mech.mania.engine.domain.model import item_pb2
from mech.mania.starter_pack.domain.model.items.status_modifier import StatusModifier
from mech.mania.starter_pack.domain.model.items.wearable import Wearable


class Clothes(Wearable):
    def __init__(self, clothes_proto: item_pb2.Clothes):
        super().__init__(StatusModifier(kwargs={'status_modifier_proto': clothes_proto.stats}))
        self.turns_to_deletion = clothes_proto.turns_to_deletion