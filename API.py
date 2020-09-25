import requests
import sys
from protos import api_pb2
from protos import character_pb2
from protos import game_pb2
API_SERVER_URL = "http://127.0.0.1:8082/api/"

"""
Finds a path from start to end in the current game state.

@param start: The position to start from
@param end: The position to end at
@return A list of Position objects from start to end or an empty list if no path is possible.
*/
"""
def pathFinding(gameState, start, end):
    if isinstance(gameState, game_pb2.GameState) and isinstance(start, character_pb2.Position) and isinstance(end, character_pb2.Position):
        url = API_SERVER_URL + "pathFinding"
        payload = api_pb2.APIPathFindingRequest()
        payload.gameState.CopyFrom(gameState)
        payload.start.CopyFrom(start)
        payload.end.CopyFrom(end)

        response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())
        APIresponse = api_pb2.APIPathFindingResponse()
        APIresponse.ParseFromString(response.content)

        if APIresponse.status.status != 200:
            return APIresponse.status
        return APIresponse.path
    else:
        return None

"""
Finds all enemies around a given position and sorts them by distance

@param position: The center position to search around
@return A List of Characters sorted by distance from the given position
"""
def findEnemiesByDistance(gameState, position, player_name):
    if isinstance(gameState, game_pb2.GameState) and isinstance(position, character_pb2.Position) and isinstance(player_name, str):
        url = API_SERVER_URL + "findEnemiesByDistance"
        payload = api_pb2.APIFindEnemiesByDistanceRequest()
        payload.gameState.CopyFrom(gameState)
        payload.position.CopyFrom(position)
        payload.player_name = player_name

        response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())

        APIresponse = api_pb2.APIFindEnemiesByDistanceResponse()
        APIresponse.ParseFromString(response.content)
        if APIresponse.status.status != 200:
            return APIresponse.status
        return APIresponse.enemies
    else:
        return None

"""
Returns a list of nearby monsters sorted by their total XP

@param position: The center position to search around
@return A List of Monster objects sorted by XP
"""
def findMonstersByExp(gameState, position):
    if isinstance(gameState, game_pb2.GameState) and isinstance(position, character_pb2.Position):
        url = API_SERVER_URL + "findMonstersByExp"
        payload = api_pb2.APIFindMonstersByExpRequest()
        payload.gameState.CopyFrom(gameState)
        payload.position.CopyFrom(position)

        response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())

        APIresponse = api_pb2.APIFindMonstersByExpResponse()
        APIresponse.ParseFromString(response.content)
        if APIresponse.status.status != 200:
            return APIresponse.status
        return APIresponse.monsters
    else:
        return None

"""
Finds all items within a given range of the given position

@param position: The position around which to search
@param range: The range to search within
@return A List of Items found in the search
"""
def findItemsInRangeByDistance(gameState, position, player_name, range):
    if isinstance(gameState, game_pb2.GameState) and isinstance(position, character_pb2.Position) and isinstance(player_name, str) and isinstance(range, int):
        url = API_SERVER_URL + "findItemsInRangeByDistance"
        payload = api_pb2.APIFindItemsInRangeByDistanceRequest()
        payload.gameState.CopyFrom(gameState)
        payload.position.CopyFrom(position)
        payload.player_name = player_name
        payload.range = range

        response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())
        APIresponse = api_pb2.APIFindItemsInRangeByDistanceResponse()
        APIresponse.ParseFromString(response.content)
        if APIresponse.status.status != 200:
            return APIresponse.status
        return (APIresponse.items, APIresponse.positions)
    else:
        return None

"""
Finds a list of enemies that would be in range of an attack from your current weapon if you were at the given position

@param position: The position to assume you are at
@return A List of Characters sorted by distance.
"""
def findEnemiesInRangeOfAttackByDistance(gameState, position, player_name):
    if isinstance(gameState, game_pb2.GameState) and isinstance(position, character_pb2.Position) and isinstance(player_name, str):
        url = API_SERVER_URL + "findEnemiesInRangeOfAttackByDistance"
        payload = api_pb2.APIFindEnemiesInRangeOfAttackByDistanceRequest()
        payload.gameState.CopyFrom(gameState)
        payload.position.CopyFrom(position)
        payload.player_name = player_name

        response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())
        APIresponse = api_pb2.APIFindEnemiesInRangeOfAttackByDistanceResponse()
        APIresponse.ParseFromString(response.content)
        if APIresponse.status.status != 200:
            return APIresponse.status
        return APIresponse.enemies
    else:
        return None

"""
Finds all enemies that would be hit by your attack if you chose the given position
as your actionPosition in an ATTACK decision this turn.

@param position: The position to test your attack at
@return A List of Characters who would be hit by your attack
"""
def findAllEnemiesHit(gameState, position, player_name):
    if isinstance(gameState, game_pb2.GameState) and isinstance(position, character_pb2.Position) and isinstance(player_name, str):
        url = API_SERVER_URL + "findAllEnemiesHit"
        payload = api_pb2.APIFindAllEnemiesHitRequest()
        payload.gameState.CopyFrom(gameState)
        payload.position.CopyFrom(position)
        payload.player_name = player_name

        response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())
        APIresponse = api_pb2.APIFindAllEnemiesHitResponse()
        APIresponse.ParseFromString(response.content)
        if APIresponse.status.status != 200:
            return APIresponse.status
        return APIresponse.enemies_hit
    else:
        return None

"""
Determines if the given position is in the attack range of any enemy

@param position: the position to test the safety of
@return True if any enemy can attack in one turn, False otherwise
"""
def inRangeOfAttack(gameState, position, player_name):
    if isinstance(gameState, game_pb2.GameState) and isinstance(position, character_pb2.Position) and isinstance(player_name, str):
        url = API_SERVER_URL + "inRangeOfAttack"
        payload = api_pb2.APIInRangeOfAttackRequest()
        payload.gameState.CopyFrom(gameState)
        payload.position.CopyFrom(position)
        payload.player_name = player_name

        response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())
        APIresponse = api_pb2.APIInRangeOfAttackResponse()
        APIresponse.ParseFromString(response.content)
        if APIresponse.status.status != 200:
            return APIresponse.status
        return APIresponse.inRangeOfAttack
    else:
        return None

"""
Finds the closest portal to the given position

@param position: The position to begin searching from
@return A Position representing the location of the closest portal, or null if an error occurred.
"""
def findClosestPortal(gameState, position):
    if isinstance(gameState, game_pb2.GameState) and isinstance(position, character_pb2.Position):
        url = API_SERVER_URL + "findClosestPortal"
        payload = api_pb2.APIFindClosestPortalRequest()
        payload.gameState.CopyFrom(gameState)
        payload.position.CopyFrom(position)

        response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())
        APIresponse = api_pb2.APIFindClosestPortalResponse()
        APIresponse.ParseFromString(response.content)
        if APIresponse.status.status != 200:
            return APIresponse.status
        return APIresponse.portal
    else:
        return None

"""
@return The list of current players sorted by total XP
"""
def leaderBoard(gameState):
    if isinstance(gameState, game_pb2.GameState):
        url = API_SERVER_URL + "leaderBoard"
        payload = api_pb2.APILeaderBoardRequest()
        payload.gameState.CopyFrom(gameState)

        response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())
        APIresponse = api_pb2.APILeaderBoardResponse()
        APIresponse.ParseFromString(response.content)
        if APIresponse.status.status != 200:
            return APIresponse.status
        return APIresponse.leaderBoard
    else:
        return None
