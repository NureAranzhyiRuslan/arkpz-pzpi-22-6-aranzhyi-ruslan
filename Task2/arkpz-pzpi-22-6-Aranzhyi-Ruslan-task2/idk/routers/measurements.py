from fastapi import APIRouter

from idk.dependencies import SensorAuthDep
from idk.models import Measurement
from idk.schemas.measurements import AddMeasurementRequest

router = APIRouter(prefix="/measurements")


@router.post("", status_code=204)
async def add_measurement(sensor: SensorAuthDep, data: AddMeasurementRequest):
    await Measurement.create(sensor=sensor, **data.model_dump())