from pydantic import BaseModel


class AddSensorRequest(BaseModel):
    city: str
    name: int | str


class SensorInfo(BaseModel):
    id: int
    secret_key: str
    city: str
    name: str


class EditSensorRequest(AddSensorRequest):
    city: str | None = None
    name: str | None = None