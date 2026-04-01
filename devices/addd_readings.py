import random

import requests

from api import apis
from auth.auth import Auth

device_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJkZXZpY2VfaWQiOjEwMSwic3ViIjoiZGV2aWNlOjEwMTp1c2VyOjMiLCJleHAiOjE3ODM3MDc2ODMsIm5iZiI6MTc3NTA2NzY4MywiaWF0IjoxNzc1MDY3NjgzfQ.qrWDi2eevZqCc427IH1KUIrxQ0uBlRDEE8AzlBbamF4"

URL = "http://localhost:8080/api/readings"


def add_reading():
    voltage_range = [220, 240]
    current_range = [0, 10]
    payload = {
        "voltage": round(random.uniform(*voltage_range), 2),
        "current": round(random.uniform(*current_range), 2),
    }
    r = requests.post(
        URL, json=payload, headers={"Authorization": f"Bearer {device_token}"}
    )
    if r.status_code == 201:
        print(f"Reading added successfully: {payload}")
    else:
        print(f"Failed to add reading: {r.status_code} - {r.text}")


if __name__ == "__main__":
    import time

    while True:
        try:
            add_reading()
            time.sleep(2)
        except Exception as e:
            print(f"Error adding reading: {e}")
            time.sleep(1)
