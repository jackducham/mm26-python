import requests
from mech.mania.engine.domain.model import api_pb2
from mech.mania.engine.domain.model import character_pb2
from mech.mania.engine.domain.model import game_pb2
from mech.mania.engine.domain.model import item_pb2
from mech.mania.starter_pack.domain.model.characters import position
from mech.mania.starter_pack.domain.model.characters import character
from mech.mania.starter_pack.domain.model.characters import player
from mech.mania.starter_pack.domain.model.characters import monster
from mech.mania.starter_pack.domain.model.items import accessory
from mech.mania.starter_pack.domain.model.items import clothes
from mech.mania.starter_pack.domain.model.items import consumable
from mech.mania.starter_pack.domain.model.items import hat
from mech.mania.starter_pack.domain.model.items import shoes
from mech.mania.starter_pack.domain.model.items import weapon


class API:
    def __init__(self, game_state, player_name):
        self.game_state = game_state.build_proto_class()
        self.player_name = player_name
        self.API_SERVER_URL = "http://engine-test.mechmania.io:8082/api/"

    def find_path(self, start, end):
        """
        Finds a path from start to end in the current game state.

        @param start: The position to start from
        @param end: The position to end at
        @return A list of Position objects from start to end or an empty list if no path is possible.
        */
        """
        if isinstance(start, position.Position) and isinstance(end, position.Position):
            url = self.API_SERVER_URL + "pathFinding"
            payload = api_pb2.APIPathFindingRequest()
            payload.gameState.CopyFrom(self.game_state)
            payload.start.CopyFrom(start.build_proto_class())
            payload.end.CopyFrom(end.build_proto_class())

            response = requests.post(url, headers={'Content-Type': 'application/protobuf'},
                                     data=payload.SerializeToString())
            APIresponse = api_pb2.APIPathFindingResponse()
            APIresponse.ParseFromString(response.content)

            if APIresponse.status.status != 200:
                return APIresponse.status

            path = []
            for tile in APIresponse.path:
                path.append(position.Position(tile))
            return path
        else:
            return None

    def find_enemies_by_distance(self, pos):
        """
        Finds all enemies around a given position and sorts them by distance

        @param position: The center position to search around
        @return A List of Characters sorted by distance from the given position
        """
        if isinstance(pos, position.Position):
            url = self.API_SERVER_URL + "findEnemiesByDistance"
            payload = api_pb2.APIFindEnemiesByDistanceRequest()
            payload.gameState.CopyFrom(self.game_state)
            payload.position.CopyFrom(pos.build_proto_class())
            payload.player_name = self.player_name

            response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())

            APIresponse = api_pb2.APIFindEnemiesByDistanceResponse()
            APIresponse.ParseFromString(response.content)
            if APIresponse.status.status != 200:
                return APIresponse.status

            enemies = []
            for enemy in APIresponse.enemies:
                enemies.append(character.Character(enemy))
            return enemies
        else:
            return None

    def findMonstersByExp(self, pos):
        """
        Returns a list of nearby monsters sorted by their total XP

        @param position: The center position to search around
        @return A List of Monster objects sorted by XP
        """
        if isinstance(pos, position.Position):
            url = self.API_SERVER_URL + "findMonstersByExp"
            payload = api_pb2.APIFindMonstersByExpRequest()
            payload.gameState.CopyFrom(self.game_state)
            payload.position.CopyFrom(pos.build_proto_class())

            response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())

            APIresponse = api_pb2.APIFindMonstersByExpResponse()
            APIresponse.ParseFromString(response.content)
            if APIresponse.status.status != 200:
                return APIresponse.status

            monsters = []
            for m in APIresponse.monsters:
                monsters.append(monster.Monster(m))
            return monsters
        else:
            return None

    def find_items_in_range_by_distance(self, pos, range):
        """
        Finds all items within a given range of the given position

        @param position: The position around which to search
        @param range: The range to search within
        @return A List of Items found in the search
        """
        if isinstance(pos, position.Position) and isinstance(range, int):
            url = self.API_SERVER_URL + "findItemsInRangeByDistance"
            payload = api_pb2.APIFindItemsInRangeByDistanceRequest()
            payload.gameState.CopyFrom(self.game_state)
            payload.position.CopyFrom(pos.build_proto_class())
            payload.player_name = self.player_name
            payload.range = range

            response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())
            APIresponse = api_pb2.APIFindItemsInRangeByDistanceResponse()
            APIresponse.ParseFromString(response.content)
            if APIresponse.status.status != 200:
                return APIresponse.status

            items = []
            item_positions = []
            for i in APIresponse.items:
                if i.HasField("accessory"):
                    items.append(accessory.Accessory(i.accessory))
                elif i.HasField("clothes"):
                    items.append(clothes.Clothes(i.clothes))
                elif i.HasField("consumable"):
                    items.append(consumable.Consumable(i.consumable))
                elif i.HasField("hat"):
                    items.append(hat.Hat(i.hat))
                elif i.HasField("shoes"):
                    items.append(shoes.Shoes(i.shoes))
                elif i.HasField("weapon"):
                    items.append(weapon.Weapon(i.weapon))

            for i_pos in APIresponse.positions:
                item_positions.append(position.Position(i_pos))

            return (items, item_positions)
        else:
            return None

    def find_enemies_in_range_of_attack_by_distance(self, pos):
        """
        Finds a list of enemies that would be in range of an attack from your current weapon if you were at the given position

        @param position: The position to assume you are at
        @return A List of Characters sorted by distance.
        """
        if isinstance(pos, position.Position):
            url = self.API_SERVER_URL + "findEnemiesInRangeOfAttackByDistance"
            payload = api_pb2.APIFindEnemiesInRangeOfAttackByDistanceRequest()
            payload.gameState.CopyFrom(self.game_state)
            payload.position.CopyFrom(pos.build_proto_class())
            payload.player_name = self.player_name

            response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())
            APIresponse = api_pb2.APIFindEnemiesInRangeOfAttackByDistanceResponse()
            APIresponse.ParseFromString(response.content)
            if APIresponse.status.status != 200:
                return APIresponse.status
            enemies = []
            for enemy in APIresponse.enemies:
                enemies.append(character.Character(enemy))
            return enemies
        else:
            return None

    def find_all_enemies_hit(self, pos):
        """
        Finds all enemies that would be hit by your attack if you chose the given position
        as your actionPosition in an ATTACK decision this turn.

        @param position: The position to test your attack at
        @return A List of Characters who would be hit by your attack
        """
        if isinstance(pos, position.Position):
            url = self.API_SERVER_URL + "findAllEnemiesHit"
            payload = api_pb2.APIFindAllEnemiesHitRequest()
            payload.gameState.CopyFrom(self.game_state)
            payload.position.CopyFrom(pos.build_proto_class())
            payload.player_name = self.player_name

            response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())
            APIresponse = api_pb2.APIFindAllEnemiesHitResponse()
            APIresponse.ParseFromString(response.content)
            if APIresponse.status.status != 200:
                return APIresponse.status
            enemies = []
            for enemy in APIresponse.enemies_hit:
                enemies.append(character.Character(enemy))
            return enemies
        else:
            return None

    def in_range_of_attack(self, pos):
        """
        Determines if the given position is in the attack range of any enemy

        @param position: the position to test the safety of
        @return True if any enemy can attack in one turn, False otherwise
        """
        if isinstance(pos, position.Position):
            url = self.API_SERVER_URL + "inRangeOfAttack"
            payload = api_pb2.APIInRangeOfAttackRequest()
            payload.gameState.CopyFrom(self.game_state)
            payload.position.CopyFrom(pos.build_proto_class())
            payload.player_name = self.player_name

            response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())
            APIresponse = api_pb2.APIInRangeOfAttackResponse()
            APIresponse.ParseFromString(response.content)
            if APIresponse.status.status != 200:
                return APIresponse.status
            return APIresponse.inRangeOfAttack
        else:
            return None

    def find_closest_portal(self, pos):
        """
        Finds the closest portal to the given position

        @param position: The position to begin searching from
        @return A Position representing the location of the closest portal, or null if an error occurred.
        """
        if isinstance(pos, position.Position):
            url = self.API_SERVER_URL + "findClosestPortal"
            payload = api_pb2.APIFindClosestPortalRequest()
            payload.gameState.CopyFrom(self.game_state)
            payload.position.CopyFrom(pos.build_proto_class())

            response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())
            APIresponse = api_pb2.APIFindClosestPortalResponse()
            APIresponse.ParseFromString(response.content)
            if APIresponse.status.status != 200:
                return APIresponse.status
            return position.Position(APIresponse.portal)
        else:
            return None

    def get_leaderboard(self):
        """
        @return The list of current players sorted by total XP
        """
        url = self.API_SERVER_URL + "leaderBoard"
        payload = api_pb2.APILeaderBoardRequest()
        payload.gameState.CopyFrom(self.game_state)

        response = requests.post(url, headers={'Content-Type': 'application/protobuf'}, data=payload.SerializeToString())
        APIresponse = api_pb2.APILeaderBoardResponse()
        APIresponse.ParseFromString(response.content)
        if APIresponse.status.status != 200:
            return APIresponse.status

        leaderBoard = []
        for p in APIresponse.leaderBoard:
            leaderBoard.append(player.Player(p))

        return leaderBoard
