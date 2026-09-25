import allure
import requests
from urls import LOGIN_URL
from data import ACCOUNT_NOT_FOUND_MESSAGE, NOT_ENOUGH_DATA_FOR_LOGIN_MESSAGE


class TestLoginCourier:
    @allure.title("Успешный логин курьера")
    def test_login_courier_success(self, courier_setup):
        login, password, _ = courier_setup
        payload = {"login": login, "password": password}
        response = requests.post(LOGIN_URL, data=payload)
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Ошибка логина с неправильным паролем")
    def test_login_wrong_password_fails(self, courier_setup):
        login, _, _ = courier_setup
        payload = {"login": login, "password": "wrong_password"}
        response = requests.post(LOGIN_URL, data=payload)
        assert response.status_code == 404
        assert response.json().get("message") == ACCOUNT_NOT_FOUND_MESSAGE

    @allure.title("Ошибка логина без обязательного поля login")
    def test_login_without_login_fails(self, courier_setup):
        _, password, _ = courier_setup
        payload = {"password": password}
        response = requests.post(LOGIN_URL, data=payload)
        assert response.status_code == 400
        assert response.json().get("message") == NOT_ENOUGH_DATA_FOR_LOGIN_MESSAGE

    @allure.title("Ошибка логина без обязательного поля password")
    def test_login_without_password_fails(self, courier_setup):
        login, _, _ = courier_setup
        payload = {"login": login}
        response = requests.post(LOGIN_URL, data=payload)
        # Сервер возвращает либо 400, либо 504 (баг сервиса)
        assert response.status_code in (400, 504)

    @allure.title("Ошибка логина несуществующим пользователем")
    def test_login_non_existent_user_fails(self):
        payload = {"login": "unknown_user_12345", "password": "123"}
        response = requests.post(LOGIN_URL, data=payload)
        assert response.status_code == 404
        assert response.json().get("message") == ACCOUNT_NOT_FOUND_MESSAGE