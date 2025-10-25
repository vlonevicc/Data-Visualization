import requests

API_KEY = "6S6GQ8K8UNOSFDJS"
BASE_URL = "https://www.alphavantage.co/query"

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "AAPL",
    "apikey": API_KEY
}

response = requests.get(BASE_URL, params=params)
print("Status Code:", response.status_code)

data = response.json()
print("Keys returned:", list(data.keys())[:5])