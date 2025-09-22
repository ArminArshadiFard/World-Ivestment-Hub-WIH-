import requests
import json

url = "https://api.bitrah.ir/api/v1/authentication/login"

payload = json.dumps({
    "Username": "sswan1973",
    "password": "Aa@123456789‬‬",
})
headers = {
    'Content-Type': 'application/json',
    'Accept-Language': '/fa-IR'
}

response = requests.request("POST", url, headers=headers, data=payload)
print(response.status_code)
print(response.text)
