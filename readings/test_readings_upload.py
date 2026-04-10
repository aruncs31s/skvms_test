import pytest
from pytest import mark
import requests
import random
import time

from auth.auth_test import user1
from auth.auth import Auth
from api.apis import API
from api.devices import DEVICES

pytestmark = mark.readings

@pytest.fixture
def token() -> str:
    auth = Auth()
    token = auth.get_token(user1.username, user1.password)
    return token

class TestReadingsUpload:

    def test_upload_readings_loop(self, token):
        headers = {"Authorization": f"Bearer {token}"}
        
        # 1. Create a Microcontroller Device
        mcu_data = {
            "name": f"Test Master MCU {int(time.time())}",
            "type": 1, 
            "ip_address": "192.168.1.50",
            "mac_address": "AA:BB:CC:DD:EE:11",
            "firmware_version_id": 1
        }
        res = requests.post(DEVICES, json=mcu_data, headers=headers)
        assert res.status_code in [200, 201], f"Failed to create MCU: {res.text}"
        mcu_id = res.json()["device"]["id"]

        solar_tokens = []

        # 2. Create 4 Solar Devices & Assign to MCU
        for i in range(1, 5):
            solar_data = {
                "name": f"Test Solar Panel {i} - {int(time.time())}",
                "type": 2, 
                "ip_address": "",
                "mac_address": "",
                "firmware_version_id": 1
            }
            res = requests.post(DEVICES, json=solar_data, headers=headers)
            assert res.status_code in [200, 201], f"Failed to create Solar: {res.text}"
            solar_id = res.json()["device"]["id"]
            
            # 3. Assign the solar device to the microcontroller
            conn_data = {"child_id": solar_id}
            conn_res = requests.post(f"{DEVICES}{mcu_id}/connected", json=conn_data, headers=headers)
            assert conn_res.status_code in [200, 201], f"Failed to assign connected device: {conn_res.text}"

            # 4. Generate Device Token for each solar device
            req_data = {"device_id": solar_id}
            dauth_res = requests.post(f"{API}/device-auth/token", json=req_data, headers=headers)
            assert dauth_res.status_code == 200, f"Failed to generate device token: {dauth_res.text}"
            solar_tokens.append(dauth_res.json()["token"])

        # 5. Upload readings in a while loop for 1000 entries
        count = 0
        while count < 1000:
            d_token = random.choice(solar_tokens)
            device_headers = {"Authorization": f"Bearer {d_token}"}
            
            # Generate dummy voltage and current values
            reading_data = {
                "voltage": round(random.uniform(10.0, 14.5), 2),
                "current": round(random.uniform(0.5, 5.0), 2)
            }
            
            r_res = requests.post(f"{API}/readings", json=reading_data, headers=device_headers)
            assert r_res.status_code == 201, f"Failed to upload reading: {r_res.text}"
            count += 1
            
        print(f"Successfully uploaded {count} readings across 4 devices.")
