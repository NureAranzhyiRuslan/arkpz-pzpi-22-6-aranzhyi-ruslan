from fastapi import APIRouter

from idk.dependencies import JwtAuthUserDep
from idk.schemas.user import UserInfoResponse, UserInfoEditRequest

router = APIRouter(prefix="/user")

@router.get("/info", response_model=UserInfoResponse)
async def get_user_info(user: JwtAuthUserDep):
    return user.to_json()


@router.patch("/info", response_model=UserInfoResponse)
async def edit_user_info(user: JwtAuthUserDep, data: UserInfoEditRequest):
    if update_fields := data.model_dump(exclude_defaults=True):
        await user.update_from_dict(update_fields).save(update_fields=list(update_fields.keys()))

    return user.to_json()
