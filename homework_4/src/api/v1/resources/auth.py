from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import HTTPAuthorizationCredentials

from src.api.v1.schemas.auth import AuthModel
from src.api.v1.schemas.users import UserCreate, UserFullOut
from src.services.auth import Auth
from src.services.user import UserService, get_user_service

router = APIRouter()

auth_handler = Auth()


@router.post(
    path="/signup",
    summary="Регистрация",
    status_code=201
)
def signup_user(
        user: UserCreate,
        user_service: UserService = Depends(get_user_service)
):
    user_service.check_username_is_used(user.username)
    if user_service.check_username_is_used(user.username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username is already in use",
            headers={"WWW-Authenticate": "Bearer"},
        )
    password = user.password
    user.password = auth_handler.get_password_hash(password)
    user: dict = user_service.create_user(user=user)
    full_out_user = UserFullOut(**user)
    return_data = {"msg": "User created.", "user": full_out_user}
    return return_data


@router.post("/login")
async def login_for_access_token(
        auth_model: AuthModel,
        user_service: UserService = Depends(get_user_service),
):
    user = auth_handler.authenticate_user(auth_model.username, auth_model.password, user_service)
    access_token = auth_handler.create_access_token_user(user_model=user)
    refresh_token = auth_handler.create_refresh_token_user(user_model=user)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
async def refresh_tokens(credentials: HTTPAuthorizationCredentials = Security(auth_handler.security)):
    refresh_token = credentials.credentials
    return auth_handler.refresh_tokens(refresh_token)
