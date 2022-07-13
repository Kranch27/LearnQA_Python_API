from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    # удалить пользователя по ID 2
    def test_delete_id2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response2 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response3 = MyRequests.delete("/user/2",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 400)

    # Создать пользователя, авторизоваться из-под него, удалить
    # затем попробовать получить его данные по ID
    def test_delete_new_user(self):
        # Создание пользователя
        data = self.prepare_registration_date()
        response1 = MyRequests.post("/user/", data=data)
        user_id = self.get_json_value(response1, "id")
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # Авторизация
        response2 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Удаление
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response3, 200)

        # Получение данных пользователя
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response4, 404)

    # удалить пользователя, будучи авторизованными другим пользователем.
    def test_delete_other_user_auth(self):
        # Создание пользователя
        data = self.prepare_registration_date()
        response1 = MyRequests.post("/user/", data=data)
        user_id = self.get_json_value(response1, "id")
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # Авторизация другим пользователем
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response2 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Удаление
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response3, 400)
