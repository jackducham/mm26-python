import socket
import threading

import requests
import uuid

from protos import infra_pb2

import subprocess
import unittest
import time

from src.mech.mania import GameServer

INFRA_PORT = 8080
GAME_ENGINE_IP = "localhost"
GAME_SERVER_ENDPOINT = "server"
LOCALHOST = "127.0.0.1"
INFRA_URL = "http://{}:{}/infra/player/new".format(GAME_ENGINE_IP, INFRA_PORT)
ENDGAME_URL = "http://{}:{}/infra/endgame".format(GAME_ENGINE_IP, INFRA_PORT)

GLOBAL_SERVER_RUN_STATUS = {}
GLOBAL_SERVER_NO_ERROR = {}
GLOBAL_PORT_LOCK = None

class AtomicInt():
    def __init__(self):
        self.lock = threading.Lock()
        self.atomicInt = 0

    def increment(self):
        self.lock.acquire()
        self.atomicInt += 1
        self.lock.release()

    def getValue(self):
        self.lock.acquire()
        res = self.atomicInt
        self.lock.release()
        return res

    def reset(self):
        self.lock.acquire()
        self.atomicInt = 0
        self.lock.release()

class InfraTestCase(unittest.TestCase):
    def setUp(self):
        start_game_engine()
        time.sleep(10)
        self.thread_list = []
        self.ports = []
        self.atomicInt = AtomicInt()

    def tearDown(self):
        end_game_engine()
        self.thread_list = []
        self.ports = []
        self.atomicInt.reset()
        time.sleep(10)

    def create_N_players(self, N):
        for count in range(N):
            port = get_open_port()
            self.ports.append(port)
            thread = threading.Thread(target=CreateGameServer, args=(LOCALHOST, port, self.atomicInt))
            thread.start()
            self.thread_list.append(thread)

        for port in self.ports:
            player_URL = create_player_URL(port)

            player = infra_pb2.InfraPlayer()
            player.player_name = str(uuid.uuid4())
            player.player_ip = player_URL + GAME_SERVER_ENDPOINT
            post_msg = player.SerializeToString()
            requests.post(INFRA_URL, post_msg)

    def shutdown_players(self):
        for port in self.ports:
            url = "http://127.0.0.1:" + str(port) + "/shutdown"
            requests.post(url)

        for thread in self.thread_list:
            thread.join()

    def runner(self, N, final_value, time_limit):
        self.create_N_players(N)
        wait_time = 0
        while(wait_time <= time_limit):
            time.sleep(1)
            if(self.atomicInt.getValue() >= final_value):
                self.shutdown_players()
                break
            wait_time += 1
        return self.atomicInt.getValue() >= final_value

    def test_canReceivePlayerTurn(self):
        self.assertTrue(self.runner(1, 1, 30))

    # def test_canReceiveMultiplePlayerTurns(self):
    #     self.assertTrue(self.runner(5, 5, 30))
    #
    # def test_canReceiveMultipleTurns(self):
    #     self.assertTrue(self.runner(1, 5, 30))
    #
    # def test_canReceiveMultiplePlayersMultipleTurns(self):
    #     self.assertTrue(self.runner(5, 25, 30))
    #
    # def test_canReceiveManyPlayers(self):
    #     self.assertTrue(self.runner(100, 500, 180))
    #
    # def test_canReceiveManyPlayersLongTime(self):
    #     self.assertTrue(self.runner(100, 5000, 300))

def CreateGameServer(host, url, atomicInt=None):
    GameServer(host, url, atomicInt)

def get_open_port():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind(("",0))
    soc.listen(1)
    port = soc.getsockname()[1]
    soc.close()
    return port

def create_player_URL(port):
    return "http://{}:{}/".format(GAME_ENGINE_IP, port)

def run_game_engine():
    try:
        # subprocess.call(['java', '-jar', 'MM26GameEngine.jar'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call(['java', '-jar', 'MM26GameEngine.jar'])
    except Exception as e:
        print(e)

def start_game_engine():
    thread = threading.Thread(target=run_game_engine)
    thread.start()

def end_game_engine():
    payload = {"password":""}
    requests.get(ENDGAME_URL, params=payload)

if __name__ == "__main__":
    """
    Creates <server_num> amount of game servers by launching threads that each
    create a game server.
    """

    test = unittest.TestLoader().loadTestsFromTestCase(InfraTestCase)
    unittest.TextTestRunner(verbosity=2).run(test)
