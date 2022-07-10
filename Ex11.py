import requests

class TestEx11:

    def test_ex11(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        assert response.cookies.get("HomeWork") == "hw_value", "Некорректное значение!"
