"""
Black-box tests for the Notifications API.
Tests cover:
  - Listing notifications (all and unread-only)
  - Mark single notification as read
  - Mark all notifications as read
  - Unauthenticated access rejected
"""

import pytest
import requests

from api.apis import NOTIFICATIONS, API
from auth.auth import Auth


@pytest.fixture(scope="module")
def admin_token():
    return Auth().get_token("admin", "admin123")


@pytest.fixture(scope="module")
def user_token():
    auth = Auth()
    auth.register("notiftest1", "Notif@1234")
    return auth.get_token("notiftest1", "Notif@1234")


class TestNotifications:

    def test_list_notifications_authenticated(self, admin_token):
        """Authenticated user should receive a notifications list."""
        res = requests.get(NOTIFICATIONS, headers={"Authorization": f"Bearer {admin_token}"})
        assert res.status_code == 200
        body = res.json()
        assert "notifications" in body
        assert isinstance(body["notifications"], list)
        assert "unread_count" in body

    def test_list_notifications_unread_only(self, admin_token):
        """Unread-only filter should return only unread notifications."""
        res = requests.get(
            f"{NOTIFICATIONS}?unread_only=true",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert res.status_code == 200
        body = res.json()
        assert "notifications" in body
        # All returned items should have read=False
        for n in body["notifications"]:
            assert n.get("read") is False or n.get("read") == False

    def test_list_notifications_unauthenticated(self):
        """Unauthenticated request should be rejected with 401."""
        res = requests.get(NOTIFICATIONS)
        assert res.status_code == 401

    def test_mark_all_read(self, admin_token):
        """Mark-all-read should succeed and return 200."""
        res = requests.put(
            f"{NOTIFICATIONS}/read-all",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert res.status_code == 200
        body = res.json()
        assert "message" in body

    def test_mark_all_read_then_check_unread_zero(self, admin_token):
        """After marking all read, unread_count should be 0."""
        requests.put(
            f"{NOTIFICATIONS}/read-all",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        res = requests.get(
            f"{NOTIFICATIONS}?unread_only=true",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert res.status_code == 200
        body = res.json()
        assert body.get("unread_count", 0) == 0

    def test_mark_single_nonexistent_read_fails(self, admin_token):
        """Marking a non-existent or other user's notification should fail gracefully."""
        res = requests.put(
            f"{NOTIFICATIONS}/999999999/read",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        # 400 (not found/belongs to user)
        assert res.status_code in (400, 404), res.text
