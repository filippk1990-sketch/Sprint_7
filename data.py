# Базовый шаблон заказа
ORDER_PAYLOAD = {
    "firstName": "Иван",
    "lastName": "Иванов",
    "address": "Москва, ул. Ленина, 1",
    "metroStation": 4,
    "phone": "+79991112233",
    "rentTime": 3,
    "deliveryDate": "2026-10-10",
    "comment": "Позвонить за час"
}

# Сообщения об ошибках для проверок
LOGIN_ALREADY_USED_MESSAGE = "Этот логин уже используется. Попробуйте другой."
NOT_ENOUGH_DATA_FOR_CREATE_MESSAGE = "Недостаточно данных для создания учетной записи"
ACCOUNT_NOT_FOUND_MESSAGE = "Учетная запись не найдена"
NOT_ENOUGH_DATA_FOR_LOGIN_MESSAGE = "Недостаточно данных для входа"