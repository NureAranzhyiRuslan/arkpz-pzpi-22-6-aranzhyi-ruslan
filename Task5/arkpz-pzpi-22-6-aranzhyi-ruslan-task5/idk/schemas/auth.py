from pydantic import BaseModel, EmailStr

from idk import config
from idk.models.user import UserRole


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    if config.IS_DEBUG:
        role: UserRole = UserRole.USER


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    token: str
    expires_at: int


class LoginResponse(RegisterResponse):
    ...