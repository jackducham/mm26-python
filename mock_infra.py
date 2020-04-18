import socket
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO
import time
import requests
import uuid

from protos import player_protos_pb2
from protos import infra_pb2
from strategy import Strategy

import subprocess
import unittest
import time

INFRA_PORT = 8080
GAME_ENGINE_PORT = 8080
GAME_ENGINE_IP = "localhost"
GAME_SERVER_ENDPOINT = "server"
INFRA_URL = "http://{}:{}/infra/player/new".format(GAME_ENGINE_IP, INFRA_PORT)
ENDGAME_URL = "http://{}:{}/infra/endgame".format(GAME_ENGINE_IP, GAME_ENGINE_PORT)

GLOBAL_SERVER_RUN_STATUS = {}
GLOBAL_SERVER_NO_ERROR = {}
GLOBAL_PORT_LOCK = None

class InfraTestCase(unittest.TestCase):
    def setUp(self):
        global GLOBAL_SERVER_RUN_STATUS, GLOBAL_SERVER_NO_ERROR, GLOBAL_PORT_LOCK
        GLOBAL_SERVER_RUN_STATUS = {}
        GLOBAL_SERVER_NO_ERROR = {}
        GLOBAL_PORT_LOCK = threading.Lock()
        start_game_engine()
        infra_URL = INFRA_URL
        # Give game engine 5 seconds to start up
        # Need to replace with a more reliable method
        time.sleep(10)

    def tearDown(self):
        end_game_engine()

    def test_ConnectNPlayers(self):
        server_num = 10
        thread_list = []
        for count in range(server_num):
            thread = threading.Thread(target=create_game_server)
            thread.start()
            thread_list.append(thread)

        for thread in thread_list:
            thread.join()

        values = list(GLOBAL_SERVER_NO_ERROR.values())
        self.assertTrue(all(values))

class Handler(BaseHTTPRequestHandler):

    def do_POST(self):
        """
        Gameserver will respond to any POST requests as defined below.
        Can specify endpoint by checking if self.path == /<endpoint>

        Function reads POST requests, parses payload to a playerTurn proto, and
        passes it on to a the "Strategy" class where users can define their
        decisions. Then gameserver will respond to game engine by sending a
        response message containing the playerDecision proto.
        """
        if self.path == "/" + GAME_SERVER_ENDPOINT:

            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            try:
                player_turn = player_protos_pb2.PlayerTurn()
                player_turn.ParseFromString(body)
                strategy = Strategy()
                response_msg = strategy.create_player_decision(player_turn)

                self.send_response(200)
                self.send_header("Content-Length", len(response_msg))
                self.end_headers()
                response = BytesIO()
                response.write(response_msg)

                self.wfile.write(response.getvalue())
                self.wfile.flush()

            except Exception as e:
                print(e)
                GLOBAL_SERVER_NO_ERROR[self.server] = False

            GLOBAL_SERVER_RUN_STATUS[self.server] = False

class GameServer():
    def __init__(self, game_port):
        """
        Sets up game server with given port and sends infra player information.
        """
        self.my_server = HTTPServer((GAME_ENGINE_IP, game_port), Handler)
        GLOBAL_SERVER_RUN_STATUS[self.my_server] = True
        GLOBAL_SERVER_NO_ERROR[self.my_server] = True

        player_URL = create_player_URL(game_port)
        infra_URL = INFRA_URL

        player = infra_pb2.InfraPlayer()
        player.player_name = str(uuid.uuid4())
        player.player_ip = player_URL + GAME_SERVER_ENDPOINT
        post_msg = player.SerializeToString()
        requests.post(infra_URL, post_msg)

        print("Set up gameserver on port {}!".format(game_port))
        GLOBAL_PORT_LOCK.release()
        while GLOBAL_SERVER_RUN_STATUS[self.my_server]:
            self.my_server.handle_request()



def get_open_port():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind(("",0))
    soc.listen(1)
    port = soc.getsockname()[1]
    soc.close()
    return port

def create_game_server():
    """
    Creates a game server and puts the open_port in the global ports list.
    """
    GLOBAL_PORT_LOCK.acquire()
    port = get_open_port()
    try:
        GameServer(port)
    except Exception as e:
        print("Failed to set up GameServer:", e)
        GLOBAL_PORT_LOCK.release()


def create_player_URL(port):
    return "http://{}:{}/".format(GAME_ENGINE_IP, port)

def run_game_engine():

    try:
        subprocess.call(['java', '-jar', 'MM26GameEngine-0.0.1-SNAPSHOT.jar'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #subprocess.call(['java', '-jar', 'MM26GameEngine-0.0.1-SNAPSHOT.jar'])
    except Exception as e:
        print(e)

def start_game_engine():
    thread = threading.Thread(target=run_game_engine)
    thread.start()

def end_game_engine():
    requests.get(ENDGAME_URL)

if __name__ == "__main__":
    """
    Creates <server_num> amount of game servers by launching threads that each
    create a game server.
    """

    test = unittest.TestLoader().loadTestsFromTestCase(InfraTestCase)
    unittest.TextTestRunner(verbosity=2).run(test)
