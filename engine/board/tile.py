from protos import board_pb2
from protos import item_pb2


class Tile:
    def __init__(self, proto_tile: board_pb2.Tile):
        if not isinstance(proto_tile, board_pb2.Tile):
            raise ValueError('Incorrect object type; expected board_pb2.Tile, got {}'.format(type(proto_tile)))

        self.items = []
        for item in proto_tile.items:
            # TODO: create Item class
            if isinstance(item, item_pb2.Clothes):
                # TODO create Clothes
                self.items.append(Clothes(item))
            elif isinstance(item, item_pb2.Hat):
                # TODO create Hat
                self.items.append(Hat(item))
            elif isinstance(item, item_pb2.Shoes):
                # TODO create Shoes
                self.items.append(Shoes(item))
            elif isinstance(item, item_pb2.Weapon):
                # TODO create Weapon
                self.items.append(Weapon(item))
            elif isinstance(item, item_pb2.Consumable):
                # TODO create Consumable
                self.items.append(Consumable(item))

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
