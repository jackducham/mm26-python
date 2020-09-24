FROM openjdk
COPY --from=python:3 / /

RUN pip install requests protobuf flask

COPY protos /protos
COPY MM26GameEngine.jar /MM26GameEngine.jar
COPY mock_infra.py /MockInfra.py
COPY mech/mania/starter_pack /GameServer.py
COPY mech/mania/starter_pack /strategy.py
COPY mech/mania/starter_pack /MemoryObject.py
COPY mech/mania/starter_pack /RedisWritePolicy.py
COPY mech/mania/starter_pack /SetValueResult.py

CMD ["python", "GameServer.py", "127.0.0.1", "8000"]
