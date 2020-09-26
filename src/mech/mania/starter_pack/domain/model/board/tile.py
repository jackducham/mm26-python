from engine.items.hat import Hat
from engine.items.clothes import Clothes
from engine.items.consumable import Consumable
from engine.items.shoes import Shoes
from engine.items.weapon import Weapon
from protos import board_pb2
from protos import item_pb2


class Tile:
    def __init__(self, proto_tile: board_pb2.Tile):

        self.items = []
        for item in proto_tile.items:
            if isinstance(item, item_pb2.Clothes):
                self.items.append(Clothes(item.clothes))
            elif isinstance(item, item_pb2.Hat):
                self.items.append(Hat(item.hat))
            elif isinstance(item, item_pb2.Shoes):
                self.items.append(Shoes(item.shoes))
            elif isinstance(item, item_pb2.Weapon):
                self.items.append(Weapon(item.weapon))
            elif isinstance(item, item_pb2.Consumable):
                self.items.append(Consumable(item.max_stack, item.consumable))

        if proto_tile.tile_type == board_pb2.Tile.TileType.VOID:
            self.type = "VOID"
        elif proto_tile.tile_type == board_pb2.Tile.TileType.BLANK:
            self.type = "BLANK"
        elif proto_tile.tile_type == board_pb2.Tile.TileType.IMPASSIBLE:
            self.type = "IMPASSIBLE"
        elif proto_tile.tile_type == board_pb2.Tile.TileType.PORTAL:
            self.type = "PORTAL"

    def get_items(self):
        return self.items

    def get_type(self):
        return self.type
