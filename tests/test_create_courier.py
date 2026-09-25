import requests
import random
import string
import allure
from urls import COURIER_URL, LOGIN_URL


class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        login = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
        payload = {"login": login, "password": "1234_password", "firstName": "Test"}

        response = requests.post(COURIER_URL, data=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

        # Очистка за собой
        log_res = requests.post(LOGIN_URL, data={"login": login, "password": "1234_password"})
        c_id = log_res.json().get("id")
        requests.delete(f"{COURIER_URL}/{c_id}")

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self, courier_setup):
        login, password, first_name = courier_setup
        payload = {"login": login, "password": password, "firstName": first_name}

        response = requests.post(COURIER_URL, data=payload)
        assert response.status_code == 409
        assert response.json().get("message") == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Ошибка при создании курьера без логина")
    def test_create_courier_without_login_fails(self):
        payload = {"password": "1234_password", "firstName": "Test"}
        response = requests.post(COURIER_URL, data=payload)
        assert response.status_code == 400
        assert response.json().get("message") == "Недостаточно данных для создания учетной записи"

    @allure.title("Ошибка при создании курьера без пароля")
    def test_create_courier_without_password_fails(self):
        payload = {"login": "test_user_no_pass", "firstName": "Test"}
        response = requests.post(COURIER_URL, data=payload)
        assert response.status_code == 400
        assert response.json().get("message") == "Недостаточно данных для создания учетной записи"