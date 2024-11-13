from pydantic import EmailStr, BaseModel


class UserInfoResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: int


class UserInfoEditRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
