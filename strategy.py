from protos import player_protos_pb2

class Strategy():
    def __init__(self):
        pass

    def create_player_decision(self, player_turn):
        """
        Parameters:
        player_turn (proto): A player_turn proto

        After parsing values from player_turn, construct a player_decision proto
        that will be sent back to the game engine.
        """
        player_name = player_turn.player_name
        player_increment = player_turn.increment

        player_decision = player_protos_pb2.PlayerDecision()
        player_decision.player_uuid = player_name
        player_decision.increment = player_increment + 1
        response_msg = player_decision.SerializeToString()
        
        return response_msg
