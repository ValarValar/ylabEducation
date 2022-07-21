from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials

from src.api.v1.schemas.users import UserFullOut, UserUpdate
from src.services.auth import Auth
from src.services.user import UserService, get_user_service

router = APIRouter()

auth_handler = Auth()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Security(auth_handler.security),
        user_service: UserService = Depends(get_user_service)
) -> dict:
    token = credentials.credentials
    token_data = auth_handler.decode_token(token)
    user = user_service.get_user(item_username=token_data.username)
    if user:
        user = user.dict()
    else:
        raise auth_handler.incorrect_credentials_401_exception
    return user


def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if not current_user.get("is_active"):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get(
    path="/me",
    response_model=dict,
    summary="Профиль текущего пользователя",
    tags=["users"],
)
def read_users_me(
        current_user: dict = Depends(get_current_active_user)
) -> dict:
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
    token_data = auth_handler.decode_token(token)
    current_username = token_data.username
    updated_user = user_service.update_user(update_user, current_username)

    if not updated_user:
        raise auth_handler.incorrect_credentials_401_exception

    user_full_out = UserFullOut(**updated_user.dict())
    new_access_token = auth_handler.create_access_token_user(update_user)
    return_data = {
        "msg": "Update is successful. Please use new access_token.",
        "user": user_full_out,
        "access_token": new_access_token
    }
    return return_data
