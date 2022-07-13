import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_date()

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_date(email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    # Создание пользователя с некорректным email - без символа @
    def test_create_user_not_at(self):
        data = self.prepare_registration_date('test0example.com')

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)

    # Создание пользователя без указания одного из полей
    data = [
        {'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'},
        {'password': '123', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'},
        {'password': '123', 'username': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'},
        {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'email': 'vinkotov@example.com'},
        {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa',}
    ]

    @pytest.mark.parametrize('par', data)
    def test_create_user_par(self, par):

        response = requests.post("https://playground.learnqa.ru/api/user/", data=par)

        Assertions.assert_code_status(response, 400)

    # Создание пользователя с очень коротким именем в один символ
    def test_create_user_one(self):
        data = self.prepare_registration_date(None, "1")
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)

    # Создание пользователя с очень длинным именем - длиннее 250 символов
    def test_create_user_long(self):
        data = self.prepare_registration_date(None, "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)