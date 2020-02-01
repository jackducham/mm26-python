import unittest
import websockets
import asyncio
import player_decision_pb2
import player_turn_pb2


class TestWebSocketConnections(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """
        Sets up the class with some parameters.
        """
        self.port = 8080
        self.uri = f"ws://localhost:{self.port}/player"

    async def test_initial_handshake(self):
        """
        Tests whether initial handshake can be made.
        """
        async with websockets.connect(uri) as websocket:
            # receive data
            result = await websocket.recv()

            # construct turn
            turn = player_turn_pb2.PlayerTurn()
            turn.ParseFromString(result)
            # use turn
            self.assertTrue(turn.turn == 1)


if __name__ == '__main__':
    unittest.main()
