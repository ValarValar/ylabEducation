from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials

from src.api.v1.schemas.users import UserFullOut, UserUpdate
from src.services.auth import get_auth_class
from src.services.user import UserService, get_user_service

router = APIRouter()

auth_handler = get_auth_class()


@router.get(
    path="/me",
    response_model=dict,
    summary="Профиль текущего пользователя",
    tags=["users"],
)
def read_users_me(
        credentials: HTTPAuthorizationCredentials = Security(auth_handler.security),
        user_service: UserService = Depends(get_user_service)
) -> dict:
    token = credentials.credentials
    current_user = user_service.get_current_active_user(token)
    if not current_user:
        raise auth_handler.incorrect_credentials_401_exception
    return {"user": UserFullOut(**current_user)}


@router.patch(
    path="/me",
    response_model=dict,
    summary="Профиль текущего пользователя",
    tags=["users"],
)
def update_users_me(
        update_user: UserUpdate,
        credentials: HTTPAuthorizationCredentials = Security(auth_handler.security),
        user_service: UserService = Depends(get_user_service),
) -> dict:
    token = credentials.credentials
    updated_user = user_service.update_user(update_user, token)

    if not updated_user:
        raise auth_handler.incorrect_credentials_401_exception

    user_full_out = UserFullOut(**updated_user.dict())
    new_access_token = auth_handler.create_access_token_user(user_full_out)
    return_data = {
        "msg": "Update is successful. Please use new access_token.",
        "user": user_full_out,
        "access_token": new_access_token
    }
    return return_data
