FROM openjdk
COPY --from=python:3 / /

RUN pip install requests protobuf


COPY protos /protos
COPY MM26GameEngine-0.0.1-SNAPSHOT.jar /MM26GameEngine-0.0.1-SNAPSHOT.jar
COPY mock_infra.py /mock_infra.py
COPY strategy.py /strategy.py

CMD ["python", "mock_infra.py"]
