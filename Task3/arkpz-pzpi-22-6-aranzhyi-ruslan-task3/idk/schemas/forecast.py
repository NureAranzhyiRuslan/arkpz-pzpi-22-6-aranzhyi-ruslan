from pydantic import BaseModel


class ForecastResponse(BaseModel):
    info_text: str
    temperature: float
    details: dict[str, float | str | bool]
