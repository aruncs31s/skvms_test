import requests


from api.apis import LOGIN, REGISTER ,REFRESH



class Auth:
    def register(
        self,
        username: str,
        password: str,
            )-> str:
        payload = {
            "username": username,
            "password": password
        }
        response = requests.post(REGISTER, json=payload)
        if response.status_code == 201 or response.status_code == 200:
            return "Registration successful"
        elif response.status_code == 400:
            return "Username or email already exists"
        else:
            return "Registration failed"
        
    def login(self, username, password):
        payload = {
            "username": username,
            "password": password
        }
        response = requests.post(LOGIN, json=payload)
        if  response.status_code == 200:
            return response.json()
        else:
            return None
    def get_token(self, username, password):
        payload = {
            "username": username,
            "password": password
        }
        response: requests.Response = requests.post(LOGIN, json=payload)
        if response.status_code == 200:
            return response.json().get("token")
        else:
            return None
    def get_refresh_token(self, username, password):
        payload = {
            "username": username,
            "password": password
        }
        response = requests.post(LOGIN, json=payload)
        if response.status_code == 200:
            return response.json().get("refresh_token")
        else:
            return None
    def refresh_token(self, token):
       
        payload = {
            "refresh_token": token
        }
        response = requests.post(REFRESH,json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None