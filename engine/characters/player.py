from protos import character_pb2
from protos import item_pb2
from engine.characters import character


class Player(character.Character):
    INVENTORY_SIZE = 16

    def __init__(self, player_proto: character_pb2.Player):
        if not isinstance(player_proto, character_pb2.Character):
            raise ValueError(
                'Incorrect object type; expected character_pb2.Player, got {}'.format(
                    type(
                        player_proto
                    )))

        super().__init__(player_proto.character)

        # TODO write items
        self.hat = Hat(player_proto.hat)
        self.clothes = Clothes(player_proto.clothes)
        self.shoes = Shoes(player_proto.shoes)
        self.inventory = [None] * self.INVENTORY_SIZE
        # TODO fix
        self.stats = None

        for i, item in enumerate(player_proto.inventory):
            # TODO: create Item class
            if isinstance(item, item_pb2.Clothes):
                # TODO create Clothes
                self.inventory[i] = Clothes(item)
            elif isinstance(item, item_pb2.Hat):
                # TODO create Hat
                self.inventory[i] = Hat(item)
            elif isinstance(item, item_pb2.Shoes):
                # TODO create Shoes
                self.inventory[i] = Shoes(item)
            elif isinstance(item, item_pb2.Weapon):
                # TODO create Weapon
                self.inventory[i] = Weapon(item)
            elif isinstance(item, item_pb2.Consumable):
                # TODO create Consumable
                self.inventory[i] = Consumable(item)

    def get_hat(self):
        return self.hat

    def get_clothes(self):
        return self.clothes

    def get_shoes(self):
        return self.shoes

    def get_inventory_size(self):
        return self.INVENTORY_SIZE

    def get_inventory(self):
        return self.inventory

    def get_speed(self):
        flat_change = 0
        percent_change = 0

        if self.hat is not None:
            flat_change += self.hat.get_stats().get_flat_speed_change()
            percent_change += self.hat.get_stats().get_percent_speed_change()

        if self.clothes is not None:
            flat_change += self.clothes.get_stats().get_flat_speed_change()
            percent_change += self.clothes.get_stats().get_percent_speed_change()

        if self.shoes is not None:
            flat_change += self.shoes.get_stats.get_flat_speed_change()
            percent_change += self.shoes.get_stats().get_percent_speed_change()

            if self.hat is not None and self.hat.get_hat_effect == "SHOES_BOOST":
                flat_change += self.shoes.get_stats.get_flat_speed_change()

        if self.weapon is not None:
            flat_change += self.weapon.get_stats().get_flat_speed_change()
            percent_change += self.weapon.get_stats().get_percent_speed_change()

        for active_effect in self.active_effects:
            flat_change += active_effect[0].get_flat_speed_change()
            percent_change += active_effect[0].get_percent_speed_change()

        flat_change = max(-self.base_speed, flat_change)
        percent_change = max(-1, percent_change)

        speed = (self.base_speed + flat_change) * (1 + percent_change)
        return max(1, int(speed))

    def get_max_health(self):
        flat_change = 0
        percent_change = 0

        if self.hat is not None:
            flat_change += self.hat.get_stats().get_flat_health_change()
            percent_change += self.hat.get_stats().get_percent_health_change()

        if self.clothes is not None:
            flat_change += self.clothes.get_stats().get_flat_health_change()
            percent_change += self.clothes.get_stats().get_percent_health_change()

        if self.shoes is not None:
            flat_change += self.shoes.get_stats.get_flat_health_change()
            percent_change += self.shoes.get_stats().get_percent_health_change()

        if self.weapon is not None:
            flat_change += self.weapon.get_stats().get_flat_health_change()
            percent_change += self.weapon.get_stats().get_percent_health_change()

        for active_effect in self.active_effects:
            flat_change += active_effect[0].get_flat_health_change()
            percent_change += active_effect[0].get_percent_health_change()

        flat_change = max(-self.base_max_health, flat_change)
        percent_change = max(-1, percent_change)

        max_health = (self.base_max_health + flat_change) * (1 + percent_change)
        return max(1, int(max_health))

    def get_attack(self):
        flat_change = 0
        percent_change = 0

        if self.hat is not None:
            flat_change += self.hat.get_stats().get_flat_attack_change()
            percent_change += self.hat.get_stats().get_percent_attack_change()

        if self.clothes is not None:
            flat_change += self.clothes.get_stats().get_flat_attack_change()
            percent_change += self.clothes.get_stats().get_percent_attack_change()

        if self.shoes is not None:
            flat_change += self.shoes.get_stats.get_flat_attack_change()
            percent_change += self.shoes.get_stats().get_percent_attack_change()

        if self.weapon is not None:
            flat_change += self.weapon.get_stats().get_flat_attack_change()
            percent_change += self.weapon.get_stats().get_percent_attack_change()

            if self.hat is not None and self.hat.get_hat_effect() == "WEAPON_BOOST":
                flat_change += self.weapon.get_stats().get_flat_attack_change() * 0.5

        for active_effect in self.active_effects:
            flat_change += active_effect[0].get_flat_attack_change()
            percent_change += active_effect[0].get_percent_attack_change()

        flat_change = max(-self.base_attack, flat_change)
        percent_change = max(-1, percent_change)

        attack = (self.base_attack + flat_change) * (1 + percent_change)
        return max(1, int(attack))

    def get_defense(self):
        flat_change = 0
        percent_change = 0

        if self.hat is not None:
            flat_change += self.hat.get_stats().get_flat_defense_change()
            percent_change += self.hat.get_stats().get_percent_defense_change()

        if self.clothes is not None:
            flat_change += self.clothes.get_stats().get_flat_defense_change()
            percent_change += self.clothes.get_stats().get_percent_defense_change()

            if self.hat is not None and self.hat.get_hat_effect == "CLOTHES_BOOST":
                flat_change += self.clothes.get_stats.get_flat_defense_change()

        if self.shoes is not None:
            flat_change += self.shoes.get_stats.get_flat_defense_change()
            percent_change += self.shoes.get_stats().get_percent_defense_change()

        if self.weapon is not None:
            flat_change += self.weapon.get_stats().get_flat_defense_change()
            percent_change += self.weapon.get_stats().get_percent_defense_change()

        for active_effect in self.active_effects:
            flat_change += active_effect[0].get_flat_defense_change()
            percent_change += active_effect[0].get_percent_defense_change()

        flat_change = max(-self.base_defense, flat_change)
        percent_change = max(-1, percent_change)

        defense = (self.base_defense + flat_change) * (1 + percent_change)
        return max(1, int(defense))

    def get_free_inventory_index(self):
        return -1 if None not in self.inventory else self.inventory.index(None)

    def get_extra_stats(self):
        return self.stats

    class Stats:
        def __init__(self, stats_proto: character_pb2.PlayerStats):
            if not isinstance(stats_proto, character_pb2.PlayerStats):
                raise ValueError(
                    'Incorrect object type; expected character_pb2.PlayerStats, got {}'.format(
                        type(
                            stats_proto
                        )))

            self.monsters_slain = stats_proto.monsters_slain
            self.death_count = stats_proto.death_count
            self.turns_since_joined = stats_proto.turns_since_joined

