import requests

class TestEx12:
    def test_ex12(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        assert response.headers.get("x-secret-homework-header") == "Some secret value", "Некорректное значение!"
