from engine.characters.character_decision import CharacterDecision
from flask import Flask, request
import sys
import time

from protos import player_pb2
from protos import character_pb2
from engine.game_state import GameState

from strategy import Strategy
from MemoryObject import MemoryObject


class GameServer:
    def __init__(self, url, port, testing_objects=None):
        self.url = url
        self.port = port
        self.debug = False
        self.memory = MemoryObject()
        self.strategy = Strategy(self.memory)

        if testing_objects is not None:
            self.atomicInt = testing_objects
            self.debug = True
        app = Flask(__name__)

        @app.route('/')
        def main_page():
            return "Welcome to MechMania26!"

        @app.route('/server', methods=['POST'])
        def send_decision():
            payload = request.get_data()

            player_turn = player_pb2.PlayerTurn()
            player_turn.ParseFromString(payload)

            game_state = GameState(player_turn.game_state)
            player_name = player_turn.player_name

            response_msg = character_pb2.CharacterDecision()

            try:
                decision = self.strategy.make_decision(player_name, game_state)
            except:
                print("Exception while implementing user strategy: {0}".format(sys.exc_info()[0]))
                decision = None

            if decision is not None:
                response_msg = decision.build_proto_class_character_decision()
            else:
                # Build NONE decision if contestant code failed
                response_msg.decision_type = character_pb2.NONE
                response_msg.action_position = None
                response_msg.index = -1

            if self.debug:
                self.atomicInt.increment()

            return response_msg.SerializeToString()

        @app.route('/shutdown', methods=['POST'])
        def shutdown():
            # saveAndClose Redis connection
            self.memory.save_and_close()

            delay = 10000  # ms to wait before shutting down server
            try:
                shutdown_server(delay)
            except Exception as e:
                print("Failed to shutdown GameServer: " + e)

            return 'Server shutting down...'

        def shutdown_server(delay):
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            time.sleep(delay / 1e3)
            func()

        try:
            app.run(host=self.url, port=self.port)
        except Exception as e:
            print("Failed to start GameServer: " + e)


if __name__ == "__main__":
    url = sys.argv[1]
    port = int(sys.argv[2])
    GameServer(url, port)
