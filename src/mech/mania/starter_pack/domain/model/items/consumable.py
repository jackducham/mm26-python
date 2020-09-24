from engine.items.item import Item
from engine.items.temp_status_modifier import TempStatusModifier
from protos import item_pb2


class Consumable(Item):
    def __init__(self, max_stack: int, consumable_proto: item_pb2.Consumable):
        if not isinstance(consumable_proto, item_pb2.Shoes):
            raise ValueError(
                            'Incorrect object type; expected item_pb2.Consumable, got {}'.format(
                                        type(consumable_proto)))
        super().__init__(max_stack)
        self.effect = TempStatusModifier(consumable_proto.effect)
        self.stacks = consumable_proto.stacks

    def get_stacks(self):
        return self.stacks

    def get_effect(self):
        return self.effect
