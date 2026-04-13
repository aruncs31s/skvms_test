from api.devices import MY_DEVICES_STATS
import pytest
from pytest import mark
import requests

from api.devices import DEVICES
from auth.auth import Auth
from utils.logger import get_logger

# from auth.auth import Auth
from auth.auth_test import user1


@pytest.fixture
def token() -> str:
    auth = Auth()
    token = auth.get_token(user1.username, user1.password)
    return token


pytestmark = mark.device


class TestDevices:
    def fetch_all(self,token) -> requests.Response:
        self.logger = get_logger()

        self.logger.info("fetching all devices")

        resp = requests.get(DEVICES, headers={"Authorization": f"Bearer {token}"})
        self.logger.info(f"token used: {token}")
        self.logger.info(f"all devices: {resp.json()}")

        return resp

    def test_get_all_devices(self, token):
        self.logger = get_logger()
        resp = self.fetch_all(token)
        
        self.logger.info(f"all devices: {resp.json()}")
        assert resp.status_code == 200
        devices = resp.json().get("devices", [])
        self.logger.info(f"all devices: {devices}")
        assert isinstance(devices, list)

    def test_get_stats(self, token):
        self.logger = get_logger()
        resp = requests.get(
            f"{MY_DEVICES_STATS}", headers={"Authorization": f"Bearer {token}"}
        )
        self.logger.info(f"stats: {resp.json()}")
        assert resp.status_code == 200
    def test_create_10_devices(self, token):
        self.logger = get_logger()
        for i in range(10):
            payload:dict = {
                "name": f"Device {i+1}",
                "type": 1,
                }
            resp = requests.post(
                DEVICES, json=payload, headers={"Authorization": f"Bearer {token}"}
            )
            self.logger.info(f"create device response: {resp.json()}")
            assert resp.status_code == 201  