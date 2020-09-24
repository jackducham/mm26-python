import requests
from mech.mania.engine.domain.model import api_pb2
from mech.mania.engine.domain.model import character_pb2
from mech.mania.engine.domain.model import game_pb2

API_SERVER_URL = "http://127.0.0.1:8082/api/"


def pathFinding(gameState, start, end):
    if isinstance(gameState, game_pb2.GameState) and isinstance(start, character_pb2.Position) and isinstance(end,
                                                                                                              character_pb2.Position):
        url = API_SERVER_URL + "pathFinding"
        payload = api_pb2.APIPathFindingRequest()
        payload.gameState.CopyFrom(gameState)
        payload.start.CopyFrom(start)
        payload.end.CopyFrom(end)

        response = requests.post(url, headers={'Content-Type': 'application/protobuf'},
                                 data=payload.SerializeToString())
        APIresponse = api_pb2.APIPathFindingResponse()
        APIresponse.ParseFromString(response.content)

        if APIresponse.status.status != 200:
            return APIresponse.status
        return APIresponse.path
    else:
        return None

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
