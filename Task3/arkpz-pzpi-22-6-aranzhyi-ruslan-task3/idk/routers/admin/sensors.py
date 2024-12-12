from fastapi import Query, APIRouter

from idk.dependencies import JwtAuthAdminDepN
from idk.models import Sensor, Measurement
from idk.schemas.common import PaginationResponse, PaginationQuery
from idk.schemas.measurements import MeasurementInfo
from idk.schemas.sensors import SensorInfo
from idk.utils.custom_exception import CustomMessageException

router = APIRouter(prefix="/sensors")


@router.get("", dependencies=[JwtAuthAdminDepN], response_model=PaginationResponse[SensorInfo])
async def get_sensors(query: PaginationQuery = Query()):
    db_query = Sensor.all().order_by("id")
    count = await db_query.count()
    sensors = await db_query.limit(query.page_size).offset(query.page_size * (query.page - 1))

    return {
        "count": count,
        "result": [
            await sensor.to_json()
            for sensor in sensors
        ]
    }


@router.get("/{sensor_id}", dependencies=[JwtAuthAdminDepN], response_model=SensorInfo)
async def get_sensor(sensor_id: int):
    if (sensor := await Sensor.get_or_none(id=sensor_id)) is None:
        raise CustomMessageException("Unknown sensor.", 404)

    return await sensor.to_json()


@router.delete("/{sensor_id}", dependencies=[JwtAuthAdminDepN], status_code=204)
async def delete_sensor(sensor_id: int):
    await Sensor.filter(id=sensor_id).delete()


@router.get("/{sensor_id}/measurements", dependencies=[JwtAuthAdminDepN], response_model=PaginationResponse[MeasurementInfo])
async def get_sensor_measurements(sensor_id: int, query: PaginationQuery = Query()):
    if (sensor := await Sensor.get_or_none(id=sensor_id)) is None:
        raise CustomMessageException("Unknown sensor.", 404)

    db_query = Measurement.filter(sensor=sensor).order_by("id")
    count = await db_query.count()
    measurements = await db_query.limit(query.page_size).offset(query.page_size * (query.page - 1))

    return {
        "count": count,
        "result": [
            measurement.to_json()
            for measurement in measurements
        ]
    }
