import requests

payload = {"password": ""}
requests.get("http://127.0.0.1:8080/infra/endgame", params=payload)
