import pytest
import urllib.request
import urllib.error
import json
import uuid

SERVER = "http://localhost:8080"
LOGIN_EP = f"{SERVER}/api/login"
REGISTER_EP = f"{SERVER}/api/register"
REFRESH_EP = f"{SERVER}/api/refresh"

def make_request(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return e.code, json.loads(body)
        except:
            return e.code, {"error": body}
    except Exception as e:
        return 0, {"error": str(e)}

@pytest.fixture(scope="module")
def setup_user():
    unique_id = str(uuid.uuid4())[:8]
    user_cred = {
        "username": f"testuser_{unique_id}",
        "password": "password123",
        "name": "Test User",
        "email": f"test_{unique_id}@example.com"
    }
    
    make_request(REGISTER_EP, user_cred)
    return user_cred

def test_login_and_refresh_token_flow(setup_user):
    # 1. Login to get both tokens
    status, data = make_request(LOGIN_EP, {
        "username": setup_user["username"],
        "password": setup_user["password"]
    })
    
    assert status == 200, f"Login failed with status {status}: {data}"
    
    assert "token" in data, "Access token missing in login response"
    assert "refresh_token" in data, "Refresh token missing in login response"
    
    first_access_token = data["token"]
    first_refresh_token = data["refresh_token"]
    
    # 2. Try the /api/refresh endpoint using the refresh token
    refresh_status, refresh_data = make_request(REFRESH_EP, {
        "refresh_token": first_refresh_token
    })
    
    assert refresh_status == 200, f"Failed to refresh token: {refresh_status} - {refresh_data}"
    
    assert "token" in refresh_data, "New access token missing in refresh response"
    assert "refresh_token" in refresh_data, "New refresh token missing in refresh response"
    
    new_access_token = refresh_data["token"]
    new_refresh_token = refresh_data["refresh_token"]
    
    assert new_access_token != "", "The newly generated access token should not be empty"
    assert new_refresh_token != "", "The newly generated refresh token should not be empty"
