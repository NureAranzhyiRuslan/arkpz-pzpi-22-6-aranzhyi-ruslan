from typing import Annotated

from fastapi import Header, Depends

from idk.models import Session, Sensor
from idk.models.user import UserRole, User
from idk.utils.custom_exception import CustomMessageException


class JWTAuthSession:
    async def __call__(
            self,
            authorization: str | None = Header(default=None),
            x_token: str | None = Header(default=None),
    ) -> Session:
        authorization = authorization or x_token
        if not authorization or (session := await Session.from_jwt(authorization)) is None:
            raise CustomMessageException("Invalid session.", 401)

        return session


JwtSessionDep = Annotated[Session, Depends(JWTAuthSession())]


class JWTAuthUser:
    def __init__(self, min_role: UserRole):
        self._min_role = min_role

    async def __call__(self, session: JwtSessionDep) -> User:
        if session.user.role < self._min_role:
            raise CustomMessageException("Insufficient privileges.", 403)

        return session.user


JwtAuthUserDep = Annotated[User, Depends(JWTAuthUser(UserRole.USER))]


async def sensor_dep(user: JwtAuthUserDep, sensor_id: int) -> Sensor:
    if (sensor := await Sensor.get_or_none(id=sensor_id, owner=user)) is None:
        raise CustomMessageException("Unknown sensor.", 404)

    return sensor


SensorDep = Annotated[Sensor, Depends(sensor_dep)]