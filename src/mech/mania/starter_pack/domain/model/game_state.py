from mech.mania.engine.domain.model import game_pb2
from mech.mania.starter_pack.domain.model.board.board import Board
from mech.mania.starter_pack.domain.model.characters.monster import Monster
from mech.mania.starter_pack.domain.model.characters.player import Player


class GameState:
    def __init__(self, game_state_proto: game_pb2.GameState):

        self.turn_num = game_state_proto.state_id

        self.board_names = {}
        for k, v in game_state_proto.board_names.items():
            self.board_names[k] = Board(v)

        self.player_names = {}
        self.monster_names = {}

        for k, v in game_state_proto.monster_names.items():
            self.monster_names[k] = Monster(v)

        for k, v in game_state_proto.player_names.items():
            self.player_names[k] = Player(v)

    def get_turn_num(self):
        return self.turn_num

    def get_pvp_board(self):
        return self.board_names['pvp']

    def get_board(self, board_id: str):
        return self.board_names[board_id]

    def get_character(self, character_id: str):
        if character_id in self.monster_names:
            return self.monster_names[character_id]

        if character_id in self.player_names:
            return self.player_names[character_id]

        return None

    def get_all_characters(self):
        return {**self.player_names, **self.monster_names}

    def get_characters_on_board(self, board_id: str):
        return self.get_monsters_on_board(board_id).extend(self.get_players_on_board(board_id))

    def get_player(self, player_id: str):
        return None if player_id not in self.player_names else self.player_names[player_id]

    def get_all_players(self):
        return self.player_names

    def get_players_on_board(self, board_id: str):
        if board_id not in self.board_names:
            return []

        return [player for player in self.player_names.values() if player.position.board_id == board_id]

    def get_monster(self, monster_id: str):
        return None if monster_id not in self.monster_names else self.monster_names[monster_id]

    def get_all_monsters(self):
        return self.monster_names

    def get_monsters_on_board(self, board_id: str):
        if board_id not in self.board_names:
            return []

        return [monster for monster in self.monster_names.values() if monster.position.board_id == board_id]

        # for name, board in self.board_names.items():
        #     game_state_builder.board_names[name].width = board.width
        #     game_state_builder.board_names[name].height = board.height
        #     game_state_builder.board_names[name].grid.extend(board.grid)
        #     game_state_builder.board_names[name].portals.extend(board.grid)
        # for name, player in self.player_names.items():
        #     character = game_state_builder.player_names[name].character
        #     character.current_health = player.current_health
        #     character.base_max_health = player.base_max_health
        #     character.experience = player.experience
        #     character.level = player.level
        #     character.base_speed = player.base_speed
        #     position = character.position
        #     position.board_id = player.position.board_id
        #     position.x = player.position.x
        #     position.y = player.position.y
        #     spawn_point = character.spawn_point
        #     character.weapon =
        #     character.active_effects_temp_status_modifier.extend()
        #     character.active_effects_source.extend()
        #     character.active_effects_is_player.extend()
        #     for player_name, damage in player.tagged_players_damage.items():
        #         character.tagged_players_damage[player_name] = damage
        #     character.is_dead = player.is_dead
        #     character.ticks_since_death = player.ticks_since_death
        #     character.name = player.name
        #     character.base_attack = player.base_attack
        #     character.base_defense = player.base_defense
        #     character.sprite = player.sprite
        #     hat = game_state_builder.player_names[name].hat
        #     clothes = game_state_builder.player_names[name].clothes
        #     shoes = game_state_builder.player_names[name].shoes
        #     game_state_builder.player_names[name].inventory.extend(player.inventory)
        # for name, monster in self.monster_names.items():
        #     game_state_builder.monster_names[name] = monster

        return game_state_builder
