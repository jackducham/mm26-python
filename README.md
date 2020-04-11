# MechMania 26 Python Starter Pack

## mock_infra.py
Unittest based attempt to mock infrastructure. Currently only 1 test that starts
up multiple game servers and connects to the server.

## strategy.py
Simple interface that allows users to parse player_turn proto, make decisions
based on those values, then create a player_decision proto to send back to game
engine.
