from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from src.api.v1.schemas.tokens import TokenData
from src.api.v1.schemas.users import UserFullOut
from src.services.user import UserService, get_user_service

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

SECRET_KEY = "b717cf81bdeaeab928ee89fc7ec8322cdfa0e10aaa1133c3c7eba5a4957f6bad"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_service: UserService = Depends(get_user_service)
) -> UserFullOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user: dict = user_service.get_user(item_username=token_data.username)
    if user is None:
        raise credentials_exception
    return UserFullOut(**user)


def get_current_active_user(current_user: UserFullOut = Depends(get_current_user)) -> UserFullOut:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get(
    path="/me",
    response_model=dict,
    summary="Профиль текущего пользователя",
    tags=["users"],
)
def read_users_me(
        current_user: UserFullOut = Depends(get_current_active_user)
) -> dict:
    return {"user": current_user}
