import requests
import pytest
import allure
from urls import ORDERS_URL
from data import ORDER_PAYLOAD


class TestCreateOrder:
    @allure.title("Создание заказа с разными вариантами цветов")
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_different_colors(self, colors):
        payload = ORDER_PAYLOAD.copy()
        payload["color"] = colors
        response = requests.post(ORDERS_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()