import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

i = 0
for r in response.history:
    i += 1
print(i)
print(response.url)
