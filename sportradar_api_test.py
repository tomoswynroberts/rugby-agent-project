import pandas
import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://api.sportradar.com/rugby-league/trial/v3/en/competitions/sr%3Acompetition%3A302/info.json"

headers = {
    "accept": "application/json",
    "x-api-key": os.environ.get("SPORTRADAR_API_KEY")
}

response = requests.get(url, headers=headers)

print(response.text)