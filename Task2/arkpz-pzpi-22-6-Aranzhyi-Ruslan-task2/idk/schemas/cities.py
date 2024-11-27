from pydantic import BaseModel


class CitySearchRequest(BaseModel):
    name: str


class CityInfoResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
