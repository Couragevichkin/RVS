import requests

url = "http://127.0.0.1:8000/number"
while True:
    number = int(input())
    payload = {"number": number}
    response = requests.post(url, json=payload)
    print(response.status_code,response.text)