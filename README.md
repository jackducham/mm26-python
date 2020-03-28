# MechMania 26 Python Starter Pack

## mock_infra.py
Creates game servers using threads and sends information about these new game servers
to the infra endpoint, which is currently located in the game engine.


## strategy.py
Simple interface that allows users to parse player_turn proto, make decisions
based on those values, then create a player_decision proto to send back to game
engine.
