import requests
import os
from datetime import datetime

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
GENDER = "male"
WEIGHT = "107"
HEIGHT = "190"
AGE = "23"

nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ.get("SHEETY_ENDPOINT")

nutritionix_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

nutritionix_text = input("Tell me what you did: ")

nutritionix_parameters = {
    "query": nutritionix_text,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}

nutritionix_response = requests.post(url=nutritionix_endpoint, json=nutritionix_parameters, headers=nutritionix_headers)
print(nutritionix_response.json())

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in nutritionix_response.json()["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

bearer_headers = {
    "Authorization": f"Bearer {os.environ.get('SHEETY_TOKEN')}"
}

requests.post(url=sheet_endpoint, json=sheet_inputs, headers=bearer_headers)
