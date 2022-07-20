from datetime import datetime, timedelta
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

from src.api.v1.schemas.tokens import Token
from src.api.v1.schemas.users import UserFullOut, UserCreate
from src.services.user import UserService, get_user_service

SECRET_KEY = "b717cf81bdeaeab928ee89fc7ec8322cdfa0e10aaa1133c3c7eba5a4957f6bad"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


@router.post(
    path="/signup",
    response_model=UserFullOut,
    summary="Регистрация",
    status_code=201
)
def signup_user(
        user: UserCreate,
        user_service: UserService = Depends(get_user_service)
) -> UserFullOut:
    user_service.check_username_is_used(user.username)
    if user_service.check_username_is_used(user.username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username is already in use",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user: dict = user_service.create_user(user=user)
    return UserFullOut(**user)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(
        username: str, password: str,
        user_service: UserService = Depends(get_user_service)
):
    user: dict = user_service.get_user(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return UserFullOut(**user)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login", response_model=Token)
async def login_for_access_token(
        user_service: UserService = Depends(get_user_service),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(form_data.username, form_data.password, user_service)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
