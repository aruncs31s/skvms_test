from dataclasses import dataclass
import pytest
from pytest import mark
from auth.auth import Auth
from utils.logger import get_logger
# Mark all tests in this module with 'auth'
pytestmark = mark.auth

@dataclass
class _User:
    username: str
    password: str


user1 = _User(username="testuser", password="testpassword")


@pytest.fixture
def auth() -> Auth:
    return Auth()


@pytest.fixture
def registered_user(auth):
    auth.register(user1.username, user1.password)
    return user1


def test_login(auth, registered_user):
    result = auth.login(registered_user.username, registered_user.password)
    assert result is not None


def test_get_token(auth, registered_user):
    token = auth.get_token(registered_user.username, registered_user.password)
    assert token is not None
    assert isinstance(token, str)


def test_refresh_token(auth: Auth, registered_user):
    l = get_logger()
    l.info(f"Testing token refresh username: {registered_user.username}, password: {registered_user.password}")
    tokens = auth.login(registered_user.username, registered_user.password)
    l.info(f"Tokens received: {tokens}")
    refresh = tokens["refresh_token"]
    new_token = auth.refresh_token(refresh)
    assert new_token is not None
    assert "token" in new_token
