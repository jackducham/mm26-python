from mech.mania.starter_pack.domain.model.characters.character_decision import CharacterDecision
from mech.mania.starter_pack.domain.model.characters.position import Position
from mech.mania.starter_pack.domain.api import API


class Strategy:
    def __init__(self, memory):
        self.memory = memory

    def make_decision(self, player_name, game_state, game_state_proto):
        """
        Parameters:
        player_name (string): The name of your player
        game_state (GameState): The current game state
        game_state_proto (game_pb2.GameState)
        """
        api = API(game_state_proto)
        # TODO: Implement your strategy here!

        decision = CharacterDecision(
            decision_type="NONE",
            action_position=None,
            action_index=-1
        )
        return decision
