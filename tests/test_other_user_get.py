import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase):
    def test_get__other_user(self):

        #Создание другого пользователя
        data = self.prepare_registration_date()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        other_user_id = self.get_json_value(response1, "id")
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # Авторизация под основным пользователем
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #Получение данных другого пользователя
        response3 = requests.get(f"https://playground.learnqa.ru/api/user/{other_user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})
        expected_fields = ["username"]
        expected_fields2 = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response3, expected_fields)
        Assertions.assert_json_has_not_key(response3, expected_fields2)
