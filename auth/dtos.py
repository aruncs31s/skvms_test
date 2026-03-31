# Auth Response DTOs
from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int
    username: str
    email: str
    name: str
    role: str

@dataclass
class AuthResponse:
    token: str
    refresh_token: str