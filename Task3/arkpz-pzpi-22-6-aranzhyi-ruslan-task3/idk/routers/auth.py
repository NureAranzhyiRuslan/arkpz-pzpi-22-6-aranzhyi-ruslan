from time import time

import bcrypt
from fastapi import APIRouter

from idk import config
from idk.dependencies import JwtSessionDep
from idk.models import User, Session
from idk.schemas.auth import RegisterResponse, RegisterRequest, LoginResponse, LoginRequest
from idk.utils.custom_exception import CustomMessageException

router = APIRouter(prefix="/auth")

@router.post("/register", response_model=RegisterResponse)
async def register(data: RegisterRequest):
    if await User.filter(email=data.email).exists():
        raise CustomMessageException("User with this email already registered!")

    password = bcrypt.hashpw(data.password.encode("utf8"), bcrypt.gensalt(config.BCRYPT_ROUNDS)).decode("utf8")
    user = await User.create(
        email=data.email,
        password=password,
        first_name=data.first_name,
        last_name=data.last_name,
    )
    if config.IS_DEBUG:
        user.role = data.role
        await user.save(update_fields=["role"])
    session = await Session.create(user=user)

    return {
        "token": session.to_jwt(),
        "expires_at": int(time() + config.AUTH_JWT_TTL),
    }


@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest):
    if (user := await User.get_or_none(email=data.email)) is None:
        raise CustomMessageException("User with this credentials is not found!")

    if not user.check_password(data.password):
        raise CustomMessageException("User with this credentials is not found!")

    session = await Session.create(user=user)
    return {
        "token": session.to_jwt(),
        "expires_at": int(time() + config.AUTH_JWT_TTL),
    }


@router.post("/logout", status_code=204)
async def logout_user(session: JwtSessionDep):
    await session.delete()
