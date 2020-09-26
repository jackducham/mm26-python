from engine.items.item import Item
from engine.items.status_modifier import StatusModifier


class Wearable(Item):
    def __init__(self, stats: StatusModifier):
        super().__init__(1)
        self.stats = stats

    def get_stats(self):
        return self.stats
