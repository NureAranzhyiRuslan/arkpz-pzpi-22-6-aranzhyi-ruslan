from pydantic import EmailStr, BaseModel

from idk.utils.enums import TemperatureUnits, Locale


class UserInfoResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: int
    locale: Locale
    temperature_units: TemperatureUnits


class UserInfoEditRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    locale: Locale | None = None
    temperature_units: TemperatureUnits | None = None
