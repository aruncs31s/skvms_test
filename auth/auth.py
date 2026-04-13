import requests

from api.apis import LOGIN, REFRESH, REGISTER
from utils.logger import get_logger


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
            # Treat duplicate registration as idempotent for test runs.
            if self.login(username, password) is not None:
                return "Username already exists"
            return "Registration failed"
        else:
            return "Registration failed"

    def login(self, username, password):
        payload = {"username": username, "password": password}
        self.logger.info(f"logging in user username: {username} , password: {password}")
        response = requests.post(LOGIN, json=payload)
        if response.status_code == 200:
            self.logger.info(f"login successful")
            return response.json()
        elif response.status_code == 401:
            self.logger.info(f"login failed: Invalid credentials")
            try:
                self.logger.info(f"response: {response.json()}")
            except requests.exceptions.JSONDecodeError:
                self.logger.info(f"response (non-json): {response.text}")
            return None
        else:
            self.logger.info(f"login failed: {response.status_code}")
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
            registration_result = self.register(username, password)
            if registration_result in ("Registration successful", "Username already exists"):
                self.logger.info(f"retrying to get token")
                retry_response: requests.Response = requests.post(LOGIN, json=payload)
                if retry_response.status_code == 200:
                    self.logger.info(f"token received successfully")
                    return retry_response.json().get("token")
            self.logger.info("token not received")
            return None

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
