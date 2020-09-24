from engine.items.status_modifier import StatusModifier
from engine.items.wearable import Wearable
from protos import item_pb2


class Shoes(Wearable):
    def __init__(self, shoes_proto: item_pb2.Shoes):
        if not isinstance(shoes_proto, item_pb2.Shoes):
            raise ValueError('Incorrect object type; expected item_pb2.Shoes, got {}'.format(type(shoes_proto)))
        super().__init__(StatusModifier(kwargs={'status_modifier_proto': shoes_proto.stats}))
