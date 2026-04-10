import requests

from api.apis import LOGIN, REFRESH, REGISTER
from utils.logger import get_logger
from pytest import mark


class Auth:
    def __init__(self):
        self.logger = get_logger()

    def register(
        self,
        username: str,
        password: str,
    ) -> str:
        payload = {"username": username, "password": password}
        self.logger.info(
            f"registering user username: {username} , password: {password}"
        )
        response = requests.post(REGISTER, json=payload)
        if response.status_code == 201 or response.status_code == 200:
            return "Registration successful"
        elif response.status_code == 400:
            return "Username or email already exists"
        else:
            return "Registration failed"

    def login(self, username, password):
        payload = {"username": username, "password": password}
        self.logger.info(f"logging in user username: {username} , password: {password}")
        response = requests.post(LOGIN, json=payload)
        if response.status_code == 200:
            self.logger.info(f"login successful")
            return response.json()
        else:
            self.logger.info(f"login failed")
            return None

    def get_token(self, username, password) -> str:
        payload = {"username": username, "password": password}
        self.logger.info(
            f"getting token for user username: {username} , password: {password}"
        )
        response: requests.Response = requests.post(LOGIN, json=payload)
        if response.status_code == 200:
            self.logger.info(f"token received successfully")
            return response.json().get("token")
        else:
            self.register(username, password)
            self.logger.info(f"retrying to get token")
            return self.get_token(username, password)

    def get_refresh_token(self, username, password):
        payload = {"username": username, "password": password}
        self.logger.info(
            f"getting refresh token for user username: {username} , password: {password}"
        )
        response = requests.post(LOGIN, json=payload)
        if response.status_code == 200:
            self.logger.info(f"refresh token received successfully")
            return response.json().get("refresh_token")
        else:
            self.logger.info(f"refresh token not received")
            return None

    def refresh_token(self, token):
        payload = {"refresh_token": token}
        self.logger.info(f"refreshing token")
        response = requests.post(REFRESH, json=payload)
        if response.status_code == 200:
            self.logger.info(f"token refreshed successfully")
            return response.json()
        else:
            self.logger.info(f"token refresh failed")
            return None

    @staticmethod
    def get_demo_token() -> str:
        from auth.auth_test import user1

        auth = Auth()
        auth.logger.info("getting demo token")
        token = auth.get_token(user1.username, user1.password)
        auth.logger.info(f"demo token: {token}")
        return token
