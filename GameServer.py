from flask import Flask, request
from protos import player_protos_pb2
import sys

from strategy import Strategy
from MemoryObject import MemoryObject

class GameServer():
    def __init__(self, url, port, testing_objects=None):
        self.url = url
        self.port = port
        self.debug = False
        self.memory = MemoryObject()
        if testing_objects is not None:
            self.atomicInt = testing_objects
            self.debug = True
        app = Flask(__name__)

        @app.route('/')
        def main_page():
            return "Welcome to MechMania26!"

        @app.route('/server', methods=['POST'])
        def send_decision():
            body = request.get_data()

            player_turn = player_protos_pb2.PlayerTurn()
            player_turn.ParseFromString(body)
            strategy = Strategy(self.memory)
            response_msg = strategy.create_player_decision(player_turn)

            if self.debug:
                self.atomicInt.increment()

            return response_msg

        @app.route('/shutdown', methods=['POST'])
        def shutdown():
            shutdown_server()
            return 'Server shutting down...'

        def shutdown_server():
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()

        try:
            app.run(host=self.url, port=self.port)
        except Exception as e:
            print("Failed to start GameServer: " + e)

if __name__ == "__main__":
    url = sys.argv[1]
    port = int(sys.argv[2])
    GameServer(url, port)
