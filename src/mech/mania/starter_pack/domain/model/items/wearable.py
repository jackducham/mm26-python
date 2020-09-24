from mech.mania.starter_pack.domain.model.items.item import Item
from mech.mania.starter_pack.domain.model.items.status_modifier import StatusModifier


class Wearable(Item):
    def __init__(self, stats: StatusModifier):
        super().__init__(1)
        self.stats = stats

    def get_stats(self):
        return self.stats
