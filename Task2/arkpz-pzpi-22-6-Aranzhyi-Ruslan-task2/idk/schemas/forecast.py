from pydantic import BaseModel


class ForecastResponse(BaseModel):
    info_text: str
    details: dict[str, int | str]
    # TODO: add other fields, like temperature array for next couple of days, etc.
