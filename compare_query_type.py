import requests
# 1
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.status_code)
print(response.text)
print("---")

# 2
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":"HEAD"})
print(response.status_code)
print(response.text)
print("---")

# 3
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":"POST"})
print(response.status_code)
print(response.text)
print("---")

# 4
rt = [requests.get, requests.post, requests.put, requests.delete]
mt = ["GET", "POST", "PUT", "DELETE"]

for i in rt:
    for e in mt:
        if i.__name__ == "get":
            response = i("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": e})
        if i.__name__ != "get":
            response = i("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": e})

        if i.__name__ == e.lower() and response.text == "Wrong method provided":
            print("Неверный ответ при совпадающих параметрах")
            print(f"Тип запроса:{i.__name__} Метод:{e}")
            print(response.status_code)
            print(response.text)
            print("---")
        if i.__name__ != e.lower() and response.text == '{"success":"!"}':
            print("Неверный ответ при НЕ совпадающих параметрах")
            print(f"Тип запроса:{i.__name__} Метод:{e}")
            print(response.status_code)
            print(response.text)
            print("---")
