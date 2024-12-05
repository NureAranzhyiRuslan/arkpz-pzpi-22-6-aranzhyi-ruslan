from fastapi import APIRouter

from idk.models import City
from idk.schemas.cities import CityInfoResponse, CitySearchRequest

router = APIRouter(prefix="/cities")

@router.post("/search", response_model=list[CityInfoResponse])
async def search_city(data: CitySearchRequest):
    cities = await City.filter(name__istartswith=data.name).limit(50)
    return [
        city.to_json()
        for city in cities
    ]