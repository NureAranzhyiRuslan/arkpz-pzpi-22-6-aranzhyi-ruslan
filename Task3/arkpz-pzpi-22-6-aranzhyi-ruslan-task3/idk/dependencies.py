from typing import Annotated

from fastapi import Header, Depends

from idk.models import Session, Sensor
from idk.models.user import UserRole, User
from idk.utils.custom_exception import CustomMessageException


async def jwt_auth_session(
        authorization: str | None = Header(default=None),
        x_token: str | None = Header(default=None),
) -> Session:
    authorization = authorization or x_token
    if not authorization or (session := await Session.from_jwt(authorization)) is None:
        raise CustomMessageException("Invalid session.", 401)

    return session


JwtSessionDep = Annotated[Session, Depends(jwt_auth_session)]


class JWTAuthUser:
    def __init__(self, min_role: UserRole):
        self._min_role = min_role

    async def __call__(self, session: JwtSessionDep) -> User:
        if session.user.role < self._min_role:
            raise CustomMessageException("Insufficient privileges.", 403)

        return session.user


JwtAuthUserDepN = Depends(JWTAuthUser(UserRole.USER))
JwtAuthUserDep = Annotated[User, JwtAuthUserDepN]

JwtAuthAdminDepN = Depends(JWTAuthUser(UserRole.ADMIN))
JwtAuthAdminDep = Annotated[User, JwtAuthAdminDepN]


async def sensor_dep(user: JwtAuthUserDep, sensor_id: int) -> Sensor:
    if (sensor := await Sensor.get_or_none(id=sensor_id, owner=user)) is None:
        raise CustomMessageException("Unknown sensor.", 404)

    return sensor


SensorDep = Annotated[Sensor, Depends(sensor_dep)]


async def sensor_auth(
        authorization: str | None = Header(default=None),
        x_token: str | None = Header(default=None),
) -> Sensor:
    authorization = authorization or x_token
    authorization = authorization.split(":")
    if len(authorization) != 3:
        raise CustomMessageException("Unknown sensor.", 404)
    sensor_key = authorization[2]
    try:
        user_id = int(authorization[0])
        sensor_id = int(authorization[1])
    except ValueError:
        raise CustomMessageException("Unknown sensor.", 404)

    if (sensor := await Sensor.get_or_none(id=sensor_id, owner__id=user_id, secret_key=sensor_key)) is None:
        raise CustomMessageException("Unknown sensor.", 404)

    return sensor


SensorAuthDep = Annotated[Sensor, Depends(sensor_auth)]