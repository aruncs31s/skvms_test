import pytest
import requests

from api.devices import DEVICES
from auth.auth import *

# from auth.auth import Auth
from auth.auth_test import user1


@pytest.fixture
def token() -> str:
    auth = Auth()
    return auth.get_token(user1.username, user1.password)


@pytest.mark.device
class TestDevices:
    def fetch_all(self) -> requests.Response:
        resp = requests.get(DEVICES, headers={"Authorization": f"Bearer {token}"})
        return resp

    def test_get_all_devices(self):
        resp = self.fetch_all()
        assert resp.status_code == 200
        devices = resp.json().get("devices", [])
        assert isinstance(devices, list)
