import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
obj = json.loads(json_text)
obj2 = obj["messages"][1]

key = "messages"
key2 = "message"

if key in obj:
    if key2 in obj2:
        print(obj2["message"])
    else:
        print(f"Ключа {key2} в JSON нет")
else:
    print(f"Ключа {key} в JSON нет")
