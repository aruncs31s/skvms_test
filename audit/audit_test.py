import pytest
import requests

from api import apis
from auth.auth import Auth

pytestmark = pytest.mark.audit

URL = apis.AUDIT


@pytest.fixture
def token() -> str:
    return Auth().get_demo_token()


class TestAudit:
    def test_get_audit(self, token):
        r = requests.get(URL, headers={"Authorization": f"Bearer {token}"})
        logs = r.json().get("logs", [])
        assert r.status_code == 200
        for log in logs:
            print(log)
            print()
            print()
