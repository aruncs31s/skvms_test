from utils.logger import get_logger
import requests
import pytest

from devices.apis import DEVICES
from api.apis import SERVER
from auth.auth_test import user1
logger = get_logger()

from auth.auth import Auth


auth = Auth()
class PublicDevices:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_public_devices(self):
        url = self.base_url
        response = requests.get(url,headers={"Authorization": f"Bearer {auth.get_token(user1.username, user1.password)}"})
        return response

if __name__ == "__main__":
    public_devices = PublicDevices(DEVICES)
    response = public_devices.get_public_devices()
    print(response.status_code)
    print(response.json())