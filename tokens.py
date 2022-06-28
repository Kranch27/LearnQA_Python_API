import time
import requests
import json

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
obj = json.loads(response.text)
token = obj["token"]
sec = obj["seconds"]
print(f"Создана задача с токеном: {token}.")

response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token":f"{token}"})
obj2 = json.loads(response2.text)

if obj2["status"] == "Job is NOT ready":
    print(f"Задача еще не готова, ждем {sec} сек.")
    time.sleep(sec)
    response3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": f"{token}"})
    obj3 = json.loads(response3.text)

    if obj3["status"] == "Job is ready" and obj3["result"] is not None:
        result = obj3["result"]
        print(f"Результат: {result}.")


