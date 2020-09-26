import logging

from mech.mania.starter_pack.domain.model.characters.character_decision import CharacterDecision
from mech.mania.starter_pack.domain.model.characters.position import Position
from mech.mania.starter_pack.domain.api import API


class Strategy:
    def __init__(self, memory):
        self.memory = memory
        self.logger = logging.getLogger('strategy')
        self.logger.setLevel(logging.DEBUG)

    def make_decision(self, player_name, game_state):
        """
        Parameters:
        player_name (string): The name of your player
        game_state (GameState): The current game state
        """
        api = API(game_state, player_name)
        my_player = game_state.get_all_players()[player_name]

        self.logger.info("In make_decision")



        decision = CharacterDecision(
            decision_type="NONE",
            action_position=None,
            action_index=-1
        )
        return decision

