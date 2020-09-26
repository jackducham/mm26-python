import logging

from mech.mania.starter_pack.domain.model.characters.character_decision import CharacterDecision
from mech.mania.starter_pack.domain.model.characters.position import Position
from mech.mania.starter_pack.domain.model.characters.player import Player
from mech.mania.starter_pack.domain.model.game_state import GameState
from mech.mania.starter_pack.domain.api import API


class Strategy:
    def __init__(self, memory):
        self.memory = memory
        self.logger = logging.getLogger('strategy')
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(level = logging.INFO)

    def make_decision(self, player_name: str, game_state: GameState) -> CharacterDecision:
        """
        Parameters:
        player_name (string): The name of your player
        game_state (GameState): The current game state
        """
        self.api = API(game_state, player_name)
        self.my_player = game_state.get_all_players()[player_name]
        self.board = game_state.get_pvp_board()
        self.curr_pos = self.my_player.get_position()

        self.logger.info("In make_decision")

        self.logger.info(f"Currently at position: ({self.curr_pos.x},{self.curr_pos.y}) on board '{self.curr_pos.board_id}'")

        last_action, type = self.memory.get_value("last_action", str)
        self.logger.info(f"last_action: '{last_action}'")

        if last_action is not None and last_action == "PICKUP":
            self.logger.info("Last action was picking up, equipping picked up object")
            self.memory.set_value("last_action", "EQUIP")
            return CharacterDecision(
                decision_type="EQUIP",
                action_position=None,
                action_index=0  # self.my_player.get_free_inventory_index()
            )

        tile_items = self.board.get_tile_at(self.curr_pos).get_items()
        if tile_items is not None and len(tile_items) > 0:
            self.logger.info("There are items on my tile, picking up item")
            self.memory.set_value("last_action", "PICKUP")
            return CharacterDecision(
                decision_type="PICKUP",
                action_position=None,
                action_index=0
            )

        weapon = self.my_player.get_weapon()
        enemies = self.api.find_enemies_by_distance(self.curr_pos)
        if enemies is None or len(enemies) == 0:
            self.logger.info("There is no enemies in range, moving to spawn point")
            self.memory.set_value("last_action", "MOVE")
            return CharacterDecision(
                decision_type="MOVE",
                action_position=self.my_player.get_spawn_point(),
                action_index=None
            )

        enemy_pos = enemies[0].get_position()
        if self.curr_pos.manhattan_distance(enemy_pos) <= weapon.get_range():
            self.logger.info("There is an enemy within weapon range, attacking")
            self.memory.set_value("last_action", "ATTACK")
            return CharacterDecision(
                decision_type="ATTACK",
                action_position=enemy_pos,
                action_index=None
            )

        self.memory.set_value("last_action", "MOVE")
        self.logger.info("Moving towards the nearest enemy")
        decision = CharacterDecision(
            decision_type="MOVE",
            action_position=self.find_position_to_move(self.my_player, enemy_pos),
            action_index=None
        )
        return decision


    # feel free to write as many helper functions as you need!
    def find_position_to_move(self, player: Player, destination: Position) -> Position:
        path = self.api.find_path(player.get_position(), destination)
        # path can be empty if player.get_position() == destination
        if len(path) == 0:
            return player.get_position()
        pos = None
        if len(path) < player.get_speed():
            pos = path[-1]
        else:
            pos = path[player.get_speed() - 1]
        return pos
