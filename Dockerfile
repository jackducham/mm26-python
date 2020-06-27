FROM openjdk
COPY --from=python:3 / /

RUN pip install requests protobuf flask

COPY protos /protos
COPY MM26GameEngine.jar /MM26GameEngine.jar
COPY MockInfra.py /MockInfra.py
COPY GameServer.py /GameServer.py
COPY strategy.py /strategy.py

CMD ["python", "GameServer.py", "127.0.0.1", "8000"]
