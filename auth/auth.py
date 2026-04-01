import requests

from api.apis import LOGIN, REFRESH, REGISTER


class Auth:
    def register(
        self,
        username: str,
        password: str,
    ) -> str:
        payload = {"username": username, "password": password}
        response = requests.post(REGISTER, json=payload)
        if response.status_code == 201 or response.status_code == 200:
            return "Registration successful"
        elif response.status_code == 400:
            return "Username or email already exists"
        else:
            return "Registration failed"

    def login(self, username, password):
        payload = {"username": username, "password": password}
        response = requests.post(LOGIN, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_token(self, username, password) -> str:
        payload = {"username": username, "password": password}
        response: requests.Response = requests.post(LOGIN, json=payload)
        if response.status_code == 200:
            return response.json().get("token")
        else:
            self.register(username, password)
            return self.get_token(username, password)

    def get_refresh_token(self, username, password):
        payload = {"username": username, "password": password}
        response = requests.post(LOGIN, json=payload)
        if response.status_code == 200:
            return response.json().get("refresh_token")
        else:
            return None

    def refresh_token(self, token):

        payload = {"refresh_token": token}
        response = requests.post(REFRESH, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    @staticmethod
    def get_demo_token() -> str:
        from auth.auth_test import user1

        auth = Auth()

        token = auth.get_token(user1.username, user1.password)
        print(f"Demo token: {token}")
        return token
