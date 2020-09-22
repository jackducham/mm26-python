from protos import character_pb2
from protos import player_pb2
from protos import game_pb2
from protos import api_pb2
import API
import sys

class Strategy():
    def __init__(self, memory):
        self.memory = memory

    def create_player_decision(self, payload):
        """
        Parameters:
        payload (proto): Game turn data sent by game engine.
        """

        player_turn = player_pb2.PlayerTurn()
        player_turn.ParseFromString(payload)

        game_state = player_turn.game_state
        player_name = player_turn.player_name

        player_decision = character_pb2.CharacterDecision()
        player_decision.decision_type = character_pb2.DecisionType.NONE
        response_msg = player_decision.SerializeToString()

        return response_msg
