import requests
from protos import player_protos_pb2

player_turn = player_protos_pb2.PlayerTurn()
player_turn.player_name = "Allen"
player_turn.increment = 1
data = player_turn.SerializeToString()

url = 'http://127.0.0.1:5000/shutdown'


x = requests.post(url, data = data)
player_dec = player_protos_pb2.PlayerDecision()
player_dec.ParseFromString(x.content)

print(player_dec)
