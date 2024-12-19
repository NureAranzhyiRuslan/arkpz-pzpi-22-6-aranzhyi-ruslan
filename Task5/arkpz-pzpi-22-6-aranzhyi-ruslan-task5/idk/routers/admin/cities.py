from fastapi import Query, APIRouter

from idk.dependencies import JwtAuthAdminDepN
from idk.models import City
from idk.schemas.cities import CityInfoResponse, CityCreateRequest, CityEditRequest
from idk.schemas.common import PaginationResponse, PaginationQuery
from idk.utils.custom_exception import CustomMessageException

router = APIRouter(prefix="/cities")


@router.get("", dependencies=[JwtAuthAdminDepN], response_model=PaginationResponse[CityInfoResponse])
async def get_cities(query: PaginationQuery = Query()):
    db_query = City.all().order_by("id")
    count = await db_query.count()
    cities = await db_query.limit(query.page_size).offset(query.page_size * (query.page - 1))

    return {
        "count": count,
        "result": [
            city.to_json()
            for city in cities
        ]
    }


@router.get("/{city_id}", dependencies=[JwtAuthAdminDepN], response_model=CityInfoResponse)
async def get_city(city_id: int):
    if (city := await City.get_or_none(id=city_id)) is None:
        raise CustomMessageException("Unknown city.", 404)

    return city.to_json()


@router.post("", dependencies=[JwtAuthAdminDepN], response_model=CityInfoResponse)
async def create_city(data: CityCreateRequest):
    city = await City.create(**data.model_dump())

    return city.to_json()


@router.patch("/{city_id}", dependencies=[JwtAuthAdminDepN], response_model=CityInfoResponse)
async def edit_city(city_id: int, data: CityEditRequest):
    if (city := await City.get_or_none(id=city_id)) is None:
        raise CustomMessageException("Unknown city.", 404)

    changes = data.model_dump(exclude_defaults=True)
    if changes:
        await city.update_from_dict(changes).save(update_fields=list(changes.keys()))

    return city.to_json()


@router.delete("/{city_id}", dependencies=[JwtAuthAdminDepN], status_code=204)
async def delete_city(city_id: int):
    await City.filter(id=city_id).delete()
