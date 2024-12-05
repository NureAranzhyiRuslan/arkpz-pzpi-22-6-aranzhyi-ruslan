from fastapi import APIRouter

from idk.dependencies import SensorAuthDep, SensorDep
from idk.models import Measurement
from idk.schemas.measurements import AddMeasurementRequest, MeasurementInfo

router = APIRouter(prefix="/measurements")


@router.post("", status_code=204)
async def add_measurement(sensor: SensorAuthDep, data: AddMeasurementRequest):
    await Measurement.create(sensor=sensor, **data.model_dump())


@router.get("/{sensor_id}", response_model=list[MeasurementInfo])
async def get_last_sensor_measurements(sensor: SensorDep):
    measurements = await Measurement.filter(sensor=sensor).order_by("-id").limit(100)
    return [
        measurement.to_json()
        for measurement in measurements
    ]