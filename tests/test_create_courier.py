import requests
import allure
from urls import COURIER_URL, LOGIN_URL
from helpers import generate_courier_credentials
from data import LOGIN_ALREADY_USED_MESSAGE, NOT_ENOUGH_DATA_FOR_CREATE_MESSAGE


class TestCreateCourier:
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        payload = generate_courier_credentials()
        response = requests.post(COURIER_URL, data=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

        # Очистка
        log_res = requests.post(LOGIN_URL, data={"login": payload["login"], "password": payload["password"]})
        c_id = log_res.json().get("id")
        requests.delete(f"{COURIER_URL}/{c_id}")

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self, courier_setup):
        login, password, first_name = courier_setup
        payload = {"login": login, "password": password, "firstName": first_name}
        response = requests.post(COURIER_URL, data=payload)
        assert response.status_code == 409
        assert response.json().get("message") == LOGIN_ALREADY_USED_MESSAGE

    @allure.title("Ошибка при создании курьера без логина")
    def test_create_courier_without_login_fails(self):
        payload = {"password": "1234_password", "firstName": "Test"}
        response = requests.post(COURIER_URL, data=payload)
        assert response.status_code == 400
        assert response.json().get("message") == NOT_ENOUGH_DATA_FOR_CREATE_MESSAGE

    @allure.title("Ошибка при создании курьера без пароля")
    def test_create_courier_without_password_fails(self):
        payload = {"login": "test_user_no_pass", "firstName": "Test"}
        response = requests.post(COURIER_URL, data=payload)
        assert response.status_code == 400
        assert response.json().get("message") == NOT_ENOUGH_DATA_FOR_CREATE_MESSAGE