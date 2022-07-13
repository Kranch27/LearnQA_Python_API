import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEditNegative(BaseCase):
    def setup(self):
        # REGISTER
        register_date = self.prepare_registration_date()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_date)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        self.email = register_date['email']
        self.first_name = register_date['firstName']
        password = register_date['password']
        self.user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_date = {
            'email': self.email,
            'password': password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login/", data=login_date)
        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

    # Попытаемся изменить данные пользователя, будучи неавторизованными
    def test_edit_no_auth(self):
        new_name = "Change name"
        response1 = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers={"x-csrf-token": "no_token"},
                                 cookies={"auth_sid": "no_cookie"},
                                 data={"firstName": new_name}
                                )
        Assertions.assert_code_status(response1, 400)

        # Проверяем что имя не изменилось
        response2 = requests.get(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                  headers={"x-csrf-token": self.token},
                                  cookies={"auth_sid": self.auth_sid}
                                  )

        Assertions.assert_json_value_by_name(
            response2,
            "firstName",
            self.first_name,
            "Wrong name of the user after edit"
        )

    # Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_other_user_auth(self):
        login_date = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login/", data=login_date)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        new_name = "Change name"
        response2 = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )
        Assertions.assert_code_status(response2, 400)

        # Проверяем что имя не изменилось
        response3 = requests.get(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid}
                                 )

        Assertions.assert_json_value_by_name(
            response3,
            "firstName",
            self.first_name,
            "Wrong name of the user after edit"
        )

    # Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем,
    # на новый email без символа @
    def test_edit_other_user_email(self):
        new_email = "mail0example.com"
        response1 = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid},
                                 data={"email": new_email}
                                 )
        Assertions.assert_code_status(response1, 400)

        # Проверяем что email не изменился
        response2 = requests.get(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid}
                                 )

        Assertions.assert_json_value_by_name(
            response2,
            "email",
            self.email,
            "Wrong email of the user after edit"
        )

    # Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем,
    # на очень короткое значение в один символ
    def test_edit_user_name_one(self):

        new_name = "1"
        response1 = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid},
                                 data={"firstName": new_name}
                                 )
        Assertions.assert_code_status(response1, 400)

        # Проверяем что имя не изменилось
        response2 = requests.get(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid}
                                 )

        Assertions.assert_json_value_by_name(
            response2,
            "firstName",
            self.first_name,
            "Wrong name of the user after edit"
        )
