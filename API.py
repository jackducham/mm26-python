import requests
from protos import api_pb2
from protos import character_pb2
from protos import game_pb2


def findEnemiesByDistance(gameState, position, player_name):
    if not isinstance(gameState, game_pb2.GameState) or not isinstance(position, character_pb2.Position) or not isinstance(player_name, str):
         
