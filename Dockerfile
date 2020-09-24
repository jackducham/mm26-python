FROM openjdk
COPY --from=python:3 / /

RUN pip install requests protobuf flask

COPY protos /protos
COPY MM26GameEngine.jar /MM26GameEngine.jar
COPY mock_infra.py /MockInfra.py
COPY src/mech /GameServer.py
COPY src/mech /strategy.py
COPY src/mech /MemoryObject.py
COPY src/mech /RedisWritePolicy.py
COPY src/mech /SetValueResult.py

CMD ["python", "GameServer.py", "127.0.0.1", "8000"]
