FROM python:3.8-alpine

WORKDIR /app/

COPY src/ src
COPY requirements.txt .

RUN pip uninstall protobuf
RUN pip install -r requirements.txt

ENV PYTHONPATH=src

CMD ["python", "src/mech/mania/starter_pack/entrypoints/game_server.py", "127.0.0.1", "8000"]
