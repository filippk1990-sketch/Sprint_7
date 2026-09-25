import pytest
import requests
from helpers import register_new_courier_and_return_login_password
from urls import LOGIN_URL, COURIER_URL

@pytest.fixture
def courier_setup():
    creds = register_new_courier_and_return_login_password()
    yield creds

    # Удаление курьера после завершения теста
    if creds:
        login_payload = {"login": creds[0], "password": creds[1]}
        login_resp = requests.post(LOGIN_URL, data=login_payload)
        if login_resp.status_code == 200:
            courier_id = login_resp.json().get("id")
            requests.delete(f"{COURIER_URL}/{courier_id}")