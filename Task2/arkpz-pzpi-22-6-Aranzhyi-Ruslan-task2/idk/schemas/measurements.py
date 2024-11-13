from pydantic import BaseModel


class AddMeasurementRequest(BaseModel):
    temperature: float
    pressure: float
