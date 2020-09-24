from mech.mania.engine.domain.model import game_pb2
from mech.mania.starter_pack.domain.model.board.board import Board
from mech.mania.starter_pack.domain.model.characters.monster import Monster
from mech.mania.starter_pack.domain.model.characters.player import Player


class GameState:
    def __init__(self, game_state_proto: game_pb2.GameState):
        if not isinstance(game_state_proto, game_pb2.GameState):
            raise ValueError('Incorrect object type; expected game_pb2.GameState, got {}'.format(
                type(game_state_proto)))

        self.board_names = {}
        for k, v in game_state_proto.board_names:
            self.board_names[k] = Board(v)

        self.turn_number = game_state_proto.turn_number

        self.player_names = {}
        self.monster_names = {}

        for k, v in game_state_proto.monster_names:
            self.monster_names[k] = Monster(v)

        for k, v in game_state_proto.player_names:
            self.player_names[k] = Player(v)

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

    def get_turn_number(self):
        return self.turn_number
