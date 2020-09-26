from mech.mania.engine.domain.model import item_pb2
from mech.mania.starter_pack.domain.model.items.item import Item
from mech.mania.starter_pack.domain.model.items.temp_status_modifier import TempStatusModifier


class Consumable(Item):
    def __init__(self, consumable_proto: item_pb2.Consumable):
        super().__init__(consumable_proto.max_stack)
        self.effect = TempStatusModifier(consumable_proto.effect)
        self.stacks = consumable_proto.stacks
        self.turns_to_deletion = consumable_proto.turns_to_deletion

    def get_stacks(self):
        return self.stacks

    def get_effect(self):
        return self.effect
