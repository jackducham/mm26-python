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

    def create_player_decision(self, payload):
        """
        Parameters:
        payload (proto): Game turn data sent by game engine.
        """

        player_turn = player_pb2.PlayerTurn()
        player_turn.ParseFromString(payload)

        game_state = GameState(player_turn.game_state)
        player_name = player_turn.player_name

        player_decision = CharacterDecision(
            # TODO implement
        )
        response_msg = player_decision.build_proto_class_character_decision().SerializeToString()

        return response_msg
