import pytest
import requests
from helpers import generate_courier_credentials
from urls import LOGIN_URL, COURIER_URL


@pytest.fixture
def courier_setup():
    creds = generate_courier_credentials()
    requests.post(COURIER_URL, data=creds)
    yield creds["login"], creds["password"], creds["firstName"]

    # Удаление курьера после теста
    login_payload = {"login": creds["login"], "password": creds["password"]}
    login_resp = requests.post(LOGIN_URL, data=login_payload)
    if login_resp.status_code == 200:
        courier_id = login_resp.json().get("id")
        requests.delete(f"{COURIER_URL}/{courier_id}")