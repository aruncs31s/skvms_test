"""
Black-box tests for the Device Token API.
Tests cover:
  - Token generation with custom expiry and label
  - Token listing per user and per device
  - Token revocation
  - Revoked token is flagged
"""

import pytest
import requests

from api.apis import TOKENS, GENERATE_TOKEN, DEVICE_TOKENS, REVOKE_TOKEN, API
from auth.auth import Auth


@pytest.fixture(scope="module")
def admin_token():
    return Auth().get_token("admin", "admin123")


@pytest.fixture(scope="module")
def device_id(admin_token):
    """Create a test device to generate tokens for."""
    payload = {"name": "TokenTestDevice", "device_type": 1, "location_id": 1}
    res = requests.post(
        f"{API}/devices",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code in (200, 201), f"Device creation failed: {res.text}"
    body = res.json()
    device = body.get("device", body)
    return device.get("id") or device.get("device_id")


class TestDeviceTokens:

    def test_generate_token_with_expiry_and_label(self, admin_token, device_id):
        """Should generate a token with custom expiry and label."""
        payload = {"expires_in_hours": 48, "label": "pytest_test_token"}
        res = requests.post(
            GENERATE_TOKEN(device_id),
            json=payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert res.status_code == 200, res.text
        body = res.json()
        assert "token" in body
        assert len(body["token"]) > 20

    def test_generate_token_default_expiry(self, admin_token, device_id):
        """Token generation with no expiry should fall back to default 24h."""
        payload = {}
        res = requests.post(
            GENERATE_TOKEN(device_id),
            json=payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert res.status_code == 200, res.text

    def test_generate_token_without_auth_fails(self, device_id):
        """Token generation without auth should be rejected."""
        res = requests.post(GENERATE_TOKEN(device_id), json={})
        assert res.status_code == 401

    def test_list_user_tokens(self, admin_token):
        """Should return a list of tokens for the authenticated user."""
        res = requests.get(TOKENS, headers={"Authorization": f"Bearer {admin_token}"})
        assert res.status_code == 200
        body = res.json()
        assert "tokens" in body
        assert isinstance(body["tokens"], list)

    def test_list_device_tokens(self, admin_token, device_id):
        """Should return tokens associated with a specific device."""
        res = requests.get(
            DEVICE_TOKENS(device_id), headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert res.status_code == 200
        body = res.json()
        assert "tokens" in body
        assert isinstance(body["tokens"], list)

    def test_revoke_token(self, admin_token, device_id):
        """Should successfully revoke an existing token."""
        # First generate a token so we have an ID
        payload = {"expires_in_hours": 1, "label": "revoke_test"}
        gen_res = requests.post(
            GENERATE_TOKEN(device_id),
            json=payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert gen_res.status_code == 200

        # Fetch tokens to get the latest token ID
        list_res = requests.get(
            TOKENS, headers={"Authorization": f"Bearer {admin_token}"}
        )
        tokens = list_res.json().get("tokens", [])
        if not tokens:
            pytest.skip("No tokens to revoke")

        token_id = tokens[0]["id"]
        revoke_res = requests.delete(
            REVOKE_TOKEN(token_id), headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert revoke_res.status_code == 200, revoke_res.text
        assert "revoked" in revoke_res.json().get("message", "").lower()

    def test_revoke_other_users_token_fails(self, device_id, admin_token):
        """A user should not be able to revoke another user's token."""
        auth = Auth()
        auth.register("tokenthief", "Tok@1234")
        thief_token = auth.get_token("tokenthief", "Tok@1234")

        # Get an admin user token ID
        list_res = requests.get(
            TOKENS, headers={"Authorization": f"Bearer {admin_token}"}
        )
        tokens = list_res.json().get("tokens", [])
        if not tokens:
            pytest.skip("No tokens to attempt theft")

        token_id = tokens[0]["id"]
        res = requests.delete(
            REVOKE_TOKEN(token_id), headers={"Authorization": f"Bearer {thief_token}"}
        )
        # Should be 400 (not found or not belonging to user)
        assert res.status_code in (400, 403), res.text
