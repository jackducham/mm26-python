import socket
from threading import Thread
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

class Handler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/server":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            playerTurn = player_protos_pb2.PlayerTurn()
            playerTurn.ParseFromString(body)
            strat = Strategy()
            response_msg = strat.createPlayerDecision(playerTurn)

            self.send_response(200)
            self.send_header("Content-Length", len(response_msg))
            self.end_headers()
            response = BytesIO()
            response.write(response_msg)
            self.wfile.write(response.getvalue())
            self.wfile.flush()

        # This is the thread that shuts down the server
        #threading.Thread(target=self.server.shutdown, daemon=True).start()



class GameServer():
    def __init__(self, port):
        self.MyServer = HTTPServer(("localhost",port), Handler)

        playerURL = createPlayerURL(port)
        infraURL = createInfraURL(8080)
        player = infra_pb2.InfraPlayer()
        player.player_name = str(uuid.uuid4())
        player.player_ip = playerURL + "server"
        post_msg = player.SerializeToString()
        requests.post(infraURL, post_msg)

        print("Set up gameserver on port {}!".format(port))

        portLock.release()
        self.MyServer.serve_forever()


def getOpenPort():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

def createGameServers():
    portLock.acquire()
    port = getOpenPort()
    ports.append(port)
    try:
        GameServer(port)
    except Exception as e:
        print("Failed to set up GameServer:", e)
        portLock.release()

def createInfraURL(port):
    return "http://localhost:{}/infra/player/new".format(port)

def createPlayerURL(port):
    return "http://localhost:{}/".format(port)

def createEndgameURL(port):
    return "http://localhost:{}/infra/endgame".format(port)

def startGameEngine():
    #subprocess.call(['java', '-jar', 'MM26GameEngine-0.0.1-SNAPSHOT.jar'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call(['java', '-jar', 'MM26GameEngine-0.0.1-SNAPSHOT.jar'])


if __name__ == "__main__":
    global threadList
    threadList = []

    global portLock
    portLock = threading.Lock()

    global ports
    ports = []

    serverNum = 5

    for i in range(serverNum):
        thread = Thread(target=createGameServers)
        thread.start()
        threadList.append(thread)

    for thread in threadList:
        thread.join()


    endgameURL = createEndgameURL(8080)
    requests.get(endgameURL)
