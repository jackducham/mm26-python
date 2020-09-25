FROM python:3.8-alpine

WORKDIR /app/

COPY src/ src
COPY requirements.txt .

RUN pip install -r requirements.txt

ENV PYTHONPATH=src

CMD ["python", "src/mech/mania/starter_pack/entrypoints/game_server.py", "0.0.0.0", "8080"]

# docker build -t mm26/python-sp .
# docker run mm26/python-sp:latest