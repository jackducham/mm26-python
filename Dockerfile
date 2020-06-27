FROM openjdk
COPY --from=python:3 / /

RUN pip install requests protobuf


COPY protos /protos
COPY MM26GameEngine.jar /MM26GameEngine.jar
COPY MockInfra.py /MockInfra.py
COPY strategy.py /strategy.py

CMD ["python", "mock_infra.py"]
