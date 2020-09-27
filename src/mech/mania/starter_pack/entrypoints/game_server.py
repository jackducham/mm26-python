import sys
import time
import traceback
import logging

from flask import Flask, request

from mech.mania.starter_pack.domain.memory.memory_object import MemoryObject
from mech.mania.starter_pack.domain.model.characters.character import Character
from mech.mania.starter_pack.domain.model.characters.character_decision import CharacterDecision
from mech.mania.starter_pack.domain.model.game_state import GameState
from mech.mania.starter_pack.domain.strategy import Strategy
from mech.mania.engine.domain.model import character_pb2
from mech.mania.engine.domain.model import player_pb2


class GameServer:
    def __init__(self, url, port, testing_objects=None):
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        self.url = url
        self.port = port
        self.debug = False
        self.memory = MemoryObject()
        self.strategy = Strategy(self.memory)

        if testing_objects is not None:
            self.atomicInt = testing_objects
            self.debug = True

        app = Flask(__name__)
        app.debug = self.debug
        app.logger.setLevel(logging.INFO)

        @app.route('/server', methods=['POST'])
        def send_decision():
            payload = request.get_data()

            player_turn = player_pb2.PlayerTurn()
            player_turn.ParseFromString(payload)

            app.logger.info(f"Received playerTurn for player: {player_turn.player_name}, turn: {player_turn.game_state.state_id}")

            game_state = GameState(player_turn.game_state)
            player_name = player_turn.player_name

            response_msg = character_pb2.CharacterDecision()

            try:
                decision = self.strategy.make_decision(player_name, game_state)
            except Exception as err:
                app.logger.info("Exception making decision:")
                traceback.print_exc()
                decision = None

            if decision is not None and isinstance(decision, CharacterDecision):
                response_msg = decision.build_proto_class_character_decision()
            else:
                # Build NONE decision if contestant code failed
                response_msg.decision_type = character_pb2.NONE
                response_msg.index = -1

                # Log incorrect return type
                app.logger.info("Recieved incorrect type for decision. Expected: CharacterDecision, Actual: " + str(type(decision)))

            if self.debug:
                self.atomicInt.increment()

            app.logger.info("Sending playerDecision")

            return response_msg.SerializeToString()

        @app.route('/shutdown', methods=['POST'])
        def shutdown():
            # saveAndClose Redis connection
            self.memory.save_and_close()

            delay = 10000  # ms to wait before shutting down server
            try:
                shutdown_server(delay)
            except Exception as e:
                app.logger.info("Failed to shutdown GameServer: " + e)

            return 'Server shutting down...'

        def shutdown_server(delay):
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            time.sleep(delay / 1e3)
            func()

        @app.route('/health', methods=['GET'])
        def health():
            return "200"

        try:
            app.run(host=self.url, port=self.port)
        except Exception as e:
            app.logger.info("Failed to start GameServer: " + e)


if __name__ == "__main__":
    url = sys.argv[1]
    port = int(sys.argv[2])
    GameServer(url, port)
