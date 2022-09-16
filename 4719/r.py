import requests
from time import sleep

with requests.session() as s:
    print(s.get("http://localhost:7776/test"))
    sleep(1)

print("hi")
