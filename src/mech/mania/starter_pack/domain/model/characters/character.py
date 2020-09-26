from mech.mania.engine.domain.model import character_pb2
from mech.mania.starter_pack.domain.model.characters.position import Position
from mech.mania.starter_pack.domain.model.items.temp_status_modifier import TempStatusModifier
from mech.mania.starter_pack.domain.model.items.weapon import Weapon


class Character:
    def __init__(self, character_proto: character_pb2.Character):

        self.character_proto = character_proto

        self.name = character_proto.name

        self.base_speed = character_proto.base_speed
        self.base_max_health = character_proto.base_max_health
        self.base_attack = character_proto.base_attack
        self.base_defense = character_proto.base_defense

        self.current_health = character_proto.current_health
        self.experience = character_proto.experience
        self.level = character_proto.level

        self.ticks_since_death = character_proto.ticks_since_death
        self.dead = character_proto.is_dead

        self.position = Position(character_proto.position)
        self.spawn_point = Position(character_proto.spawn_point)

        self.weapon = Weapon(character_proto.weapon)

        self.active_effects = []
        for tup in zip(
                        character_proto.active_effects_temp_status_modifier,
                        character_proto.active_effects_source,
                        character_proto.active_effects_is_player):
            effect = TempStatusModifier(tup[0])
            source = tup[1]
            is_player = tup[2]

            self.active_effects.append((effect, source, is_player))

        self.tagged_players_damage = character_proto.tagged_players_damage

    def get_name(self):
        return self.name

    def get_speed(self):
        flat_change = 0
        percent_change = 0
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
        for active_effect in self.active_effects:
            flat_change += active_effect[0].get_flat_health_change()
            percent_change += active_effect[0].get_percent_health_change()

        flat_change = max(-self.base_max_health, flat_change)
        percent_change = max(-1, percent_change)

        max_health = (self.base_max_health + flat_change) * (1 + percent_change)
        return max(1, int(max_health))

    def get_experience(self):
        return self.experience

    def get_attack(self):
        flat_change = 0
        percent_change = 0
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
        for active_effect in self.active_effects:
            flat_change += active_effect[0].get_flat_defense_change()
            percent_change += active_effect[0].get_percent_defense_change()

        flat_change = max(-self.base_defense, flat_change)
        percent_change = max(-1, percent_change)

        defense = (self.base_defense + flat_change) * (1 + percent_change)
        return max(1, int(defense))

    def get_current_health(self):
        return min(self.current_health, self.get_max_health())

    def get_level(self):
        return self.level

    def get_total_experience(self):
        return self.get_level() * (self.get_level() - 1) * 100 / 2 + self.get_experience()

    def is_dead(self):
        return self.dead

    def get_position(self):
        return self.position

    def get_spawn_point(self):
        return self.spawn_point

    def get_weapon(self):
        return self.weapon

    def build_proto_class(self):
        return self.character_proto
