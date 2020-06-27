# MechMania 26 Python Starter Pack

## GameServer.py
Creates a game server with the given url and port number.
Example: python GameServer.py 127.0.0.1 8000

## mock_infra.py
Unittest based attempt to mock infrastructure. Currently only 1 test that starts
up multiple game servers and connects to the server.

## strategy.py
Simple interface that allows users to parse player_turn proto, make decisions
based on those values, then create a player_decision proto to send back to game
engine.
