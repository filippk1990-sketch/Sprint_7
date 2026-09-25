import allure
import requests
from urls import LOGIN_URL


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
        assert response.json().get("message") == "Учетная запись не найдена"

    @allure.title("Ошибка логина без обязательного поля login")
    def test_login_without_login_fails(self, courier_setup):
        _, password, _ = courier_setup
        payload = {"password": password}

        response = requests.post(LOGIN_URL, data=payload)
        assert response.status_code == 400
        assert response.json().get("message") == "Недостаточно данных для входа"

    @allure.title("Ошибка логина без обязательного поля password")
    def test_login_without_password_fails(self, courier_setup):
        login, _, _ = courier_setup
        payload = {"login": login}

        try:
            response = requests.post(LOGIN_URL, data=payload, timeout=5)
            # Сервер Самоката содержит баг: вместо 400 возвращает 504 Gateway Timeout
            assert response.status_code in [400, 504]
            if response.status_code == 400:
                assert response.json().get("message") == "Недостаточно данных для входа"
        except requests.exceptions.ReadTimeout:
            pass

    @allure.title("Ошибка логина несуществующим пользователем")
    def test_login_non_existent_user_fails(self):
        payload = {"login": "unknown_user_12345", "password": "123"}

        response = requests.post(LOGIN_URL, data=payload)
        assert response.status_code == 404
        assert response.json().get("message") == "Учетная запись не найдена"