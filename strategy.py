from engine.characters.character_decision import CharacterDecision
from engine.game_state import GameState
from protos import player_pb2
from protos import game_pb2
from protos import api_pb2
import API
import sys


class Strategy:
    def __init__(self, memory):
        self.memory = memory

    def make_decision(self, player_name, game_state):
        """
        Parameters:
        player_name (string): The name of your player
        game_state (GameState): The current game state
        """

        # TODO: Implement your strategy here!

        decision = CharacterDecision(
            decision_type="NONE",
            action_position=None,
            action_index=-1
        )
        return decision
