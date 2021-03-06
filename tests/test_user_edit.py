import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

@allure.suite("Редактирование пользователя")
@allure.link("https://example.com/testcase")
class TestUserEdit(BaseCase):

    @allure.description("Тест на редактирование пользователя")
    @allure.title("Редактирование пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_just_created_user(self):
        # REGISTER
        register_date = self.prepare_registration_date()
        response1 = MyRequests.post("/user/", data=register_date)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_date['email']
        first_name = register_date['firstName']
        password = register_date['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_date = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login/", data=login_date)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Change name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid},
                                  data={"firstName": new_name}
                                  )

        Assertions.assert_code_status(response3, 200)

        # GET

        response4 = MyRequests.get(f"/user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid}
                                  )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )
