from fastapi import Query, APIRouter

from idk.dependencies import JwtAuthAdminDepN
from idk.models import Measurement
from idk.schemas.common import PaginationResponse, PaginationQuery
from idk.schemas.measurements import MeasurementInfo
from idk.utils.custom_exception import CustomMessageException

router = APIRouter(prefix="/measurements")


@router.get("", dependencies=[JwtAuthAdminDepN], response_model=PaginationResponse[MeasurementInfo])
async def get_measurements(query: PaginationQuery = Query()):
    db_query = Measurement.all().order_by("id")
    count = await db_query.count()
    measurements = await db_query.limit(query.page_size).offset(query.page_size * (query.page - 1))

    return {
        "count": count,
        "result": [
            measurement.to_json()
            for measurement in measurements
        ]
    }


@router.get("/{measurement_id}", dependencies=[JwtAuthAdminDepN], response_model=MeasurementInfo)
async def get_measurement(measurement_id: int):
    if (measurement := await Measurement.get_or_none(id=measurement_id)) is None:
        raise CustomMessageException("Unknown measurement.", 404)

    return measurement.to_json()


@router.delete("/{measurement_id}", dependencies=[JwtAuthAdminDepN], status_code=204)
async def delete_measurement(measurement_id: int):
    await Measurement.filter(id=measurement_id).delete()
