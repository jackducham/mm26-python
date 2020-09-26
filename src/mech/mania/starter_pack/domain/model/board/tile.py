from mech.mania.starter_pack.domain.model.items.hat import Hat
from mech.mania.starter_pack.domain.model.items.clothes import Clothes
from mech.mania.starter_pack.domain.model.items.consumable import Consumable
from mech.mania.starter_pack.domain.model.items.shoes import Shoes
from mech.mania.starter_pack.domain.model.items.weapon import Weapon
from mech.mania.starter_pack.domain.model.items.accessory import Accessory
from mech.mania.engine.domain.model import board_pb2
from mech.mania.engine.domain.model import item_pb2


class Tile:
    def __init__(self, proto_tile: board_pb2.Tile):

        self.proto_tile = proto_tile

        self.items = []
        for item in proto_tile.items:
            if item.HasField("clothes"):
                self.items.append(Clothes(item.clothes))
            elif item.HasField("hat"):
                self.items.append(Hat(item.hat))
            elif item.HasField("shoes"):
                self.items.append(Shoes(item.shoes))
            elif item.HasField("accessory"):
                self.items.append(Accessory(item.accessory))
            elif item.HasField("weapon"):
                self.items.append(Weapon(item.weapon))
            elif item.HasField("consumable"):
                self.items.append(Consumable(item.consumable))

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

    def build_proto_class(self):
        return self.proto_tile
