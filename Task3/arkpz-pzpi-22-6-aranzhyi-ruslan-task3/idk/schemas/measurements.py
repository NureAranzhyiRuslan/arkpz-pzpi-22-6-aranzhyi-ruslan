from pydantic import BaseModel


class AddMeasurementRequest(BaseModel):
    temperature: float
    pressure: float


class MeasurementInfo(BaseModel):
    temperature: float
    pressure: float
    timestamp: int
