SERVER = "http://localhost:8089"

API = SERVER + "/api"
REGISTER = SERVER + "/api/register"
LOGIN = SERVER + "/api/login"
REFRESH = SERVER + "/api/refresh"
LOGOUT = SERVER + "/api/logout"

# Audit
AUDIT = API + "/audit/"

# Notifications
NOTIFICATIONS = API + "/notifications"

# Tokens
TOKENS = API + "/tokens"


def DEVICE_OWNERSHIP(device_id):
    return API + f"/devices/{device_id}/ownership"


def DEVICE_TRANSFER(device_id):
    return API + f"/devices/{device_id}/transfer"


def DEVICE_TRANSFER_HISTORY(device_id):
    return API + f"/devices/{device_id}/transfer-history"


def DEVICE_PUBLIC(device_id):
    return API + f"/devices/{device_id}/public"


def DEVICE_TOKENS(device_id):
    return API + f"/devices/{device_id}/tokens"


def GENERATE_TOKEN(device_id):
    return API + f"/devices/{device_id}/token"


def REVOKE_TOKEN(token_id):
    return API + f"/tokens/{token_id}"


# device

DEVICES = API + "/devices"
