from pydantic import BaseModel

from idk.schemas.cities import CityInfoResponse


class AddSensorRequest(BaseModel):
    city: int | str
    name: str


class SensorInfo(BaseModel):
    id: int
    secret_key: str
    city: CityInfoResponse
    name: str


class EditSensorRequest(AddSensorRequest):
    city: str | None = None
    name: str | None = None