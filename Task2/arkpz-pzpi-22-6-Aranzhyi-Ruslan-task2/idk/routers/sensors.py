from fastapi import APIRouter

from idk.dependencies import JwtAuthUserDep, SensorDep
from idk.models import Sensor
from idk.schemas.sensors import SensorInfo, AddSensorRequest, EditSensorRequest

router = APIRouter(prefix="/sensors")


@router.get("", response_model=list[SensorInfo])
async def get_user_sensors(user: JwtAuthUserDep):
    return [
        sensor.to_json()
        for sensor in await Sensor.filter(owner=user)
    ]


@router.post("", response_model=SensorInfo)
async def add_sensor(user: JwtAuthUserDep, data: AddSensorRequest):
    sensor = await Sensor.create(user=user, **data.model_dump())

    return sensor.to_json()


@router.get("/{sensor_id}", response_model=SensorInfo)
async def get_sensor(sensor: SensorDep):
    return sensor.to_json()


@router.patch("/{sensor_id}", response_model=SensorInfo)
async def edit_sensor(sensor: SensorDep, data: EditSensorRequest):
    if update_fields := data.model_dump(exclude_defaults=True):
        sensor.update_from_dict(update_fields)
        await sensor.save(update_fields=list(update_fields.keys()))

    return sensor.to_json()


@router.delete("/{sensor_id}", status_code=204)
async def delete_sensor(sensor: SensorDep):
    await sensor.update(owner=None)