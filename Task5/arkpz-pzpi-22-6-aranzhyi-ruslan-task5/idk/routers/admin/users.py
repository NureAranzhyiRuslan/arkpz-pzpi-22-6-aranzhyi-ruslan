from fastapi import Query, APIRouter

from idk.dependencies import JwtAuthAdminDepN
from idk.models import User, Sensor
from idk.schemas.common import PaginationResponse, PaginationQuery
from idk.schemas.sensors import SensorInfo
from idk.schemas.user import UserInfoResponse
from idk.utils.custom_exception import CustomMessageException

router = APIRouter(prefix="/users")


@router.get("", dependencies=[JwtAuthAdminDepN], response_model=PaginationResponse[UserInfoResponse])
async def get_users(query: PaginationQuery = Query()):
    db_query = User.all().order_by("id")
    count = await db_query.count()
    users = await db_query.limit(query.page_size).offset(query.page_size * (query.page - 1))

    return {
        "count": count,
        "result": [
            user.to_json()
            for user in users
        ]
    }


@router.get("/{user_id}", dependencies=[JwtAuthAdminDepN], response_model=UserInfoResponse)
async def get_user(user_id: int):
    if (user := await User.get_or_none(id=user_id)) is None:
        raise CustomMessageException("Unknown user.", 404)

    return user.to_json()


@router.delete("/{user_id}", dependencies=[JwtAuthAdminDepN], status_code=204)
async def delete_user(user_id: int):
    await User.filter(id=user_id).delete()


@router.get("/{user_id}/sensors", dependencies=[JwtAuthAdminDepN], response_model=PaginationResponse[SensorInfo])
async def get_user_sensors(user_id: int, query: PaginationQuery = Query()):
    if (user := await User.get_or_none(id=user_id)) is None:
        raise CustomMessageException("Unknown user.", 404)

    db_query = Sensor.filter(owner=user).order_by("id")
    count = await db_query.count()
    sensors = await db_query.limit(query.page_size).offset(query.page_size * (query.page - 1))

    return {
        "count": count,
        "result": [
            await sensor.to_json()
            for sensor in sensors
        ]
    }
