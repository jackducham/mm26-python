import socket
import threading

import requests
import uuid

from protos import infra_pb2
from strategy import Strategy

import subprocess
import unittest
import time

from GameServer import GameServer
from redis import Redis

INFRA_PORT = 8080
GAME_ENGINE_IP = "localhost"
GAME_SERVER_ENDPOINT = "server"
LOCALHOST = "127.0.0.1"
INFRA_URL = "http://{}:{}/infra/player/new".format(GAME_ENGINE_IP, INFRA_PORT)
ENDGAME_URL = "http://{}:{}/infra/endgame".format(GAME_ENGINE_IP, INFRA_PORT)

GLOBAL_SERVER_RUN_STATUS = {}
GLOBAL_SERVER_NO_ERROR = {}
GLOBAL_PORT_LOCK = None

def create_player_URL(port):
    return "http://{}:{}/".format(GAME_ENGINE_IP, port)

def get_open_port():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind(("",0))
    soc.listen(1)
    port = soc.getsockname()[1]
    soc.close()
    return port

def CreateGameServer(host, url, atomicInt=None):
    GameServer(host, url, atomicInt)

port = get_open_port()
thread = threading.Thread(target=CreateGameServer, args=(LOCALHOST, port, None))
thread.start()

player_URL = create_player_URL(port)

player = infra_pb2.InfraPlayer()
player.player_name = str(uuid.uuid4())
player.player_ip = player_URL + GAME_SERVER_ENDPOINT
post_msg = player.SerializeToString()
print(requests.post(INFRA_URL, post_msg))
