from protos import player_protos_pb2

class Strategy():
    def __init__(self):
        pass

    def createPlayerDecision(self, playerTurn):
        playerName = playerTurn.player_name
        playerIncrement = playerTurn.increment

        playerDecision = player_protos_pb2.PlayerDecision()
        playerDecision.player_uuid = playerName
        playerDecision.increment = playerIncrement + 1
        response_msg = playerDecision.SerializeToString()
        return response_msg
