from pydantic import BaseModel


class CitySearchRequest(BaseModel):
    name: str


class CityInfoResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float


class CityCreateRequest(BaseModel):
    name: str
    latitude: float
    longitude: float


class CityEditRequest(CityCreateRequest):
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
