from datetime import datetime, timedelta
from datetime import timezone

from fastapi.security import OAuth2PasswordBearer
from fastcrud.exceptions.http_exceptions import UnauthorizedException
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import verify_password
from app.core.config import settings
from app.core.message import ErrorMsg
from app.services.user import crud_user

SECRET_KEY = settings.SECRET_KEY.get_secret_value()
ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


async def authenticate_user(db: AsyncSession, username_or_email: str, password: str):
    if "@" in username_or_email:
        user = await crud_user.get(db=db, email=username_or_email, is_deleted=False)
    else:
        user = await crud_user.get(db=db, username=username_or_email, is_deleted=False)

    if not user:
        raise UnauthorizedException(ErrorMsg.INVALID_CREDENTIALS)

    if not verify_password(password, user["password"]):
        raise UnauthorizedException(ErrorMsg.INVALID_CREDENTIALS)
    return user


def create_access_token(data: dict):
    token_data = data.copy()
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(UTC).replace(tzinfo=None) + expires_delta
    token_data.update({"exp": expire, "token_type": "access"})
    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    token_data = data.copy()
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    expire = datetime.now(UTC).replace(tzinfo=None) + expires_delta
    token_data.update({"exp": expire, "token_type": "refresh"})
    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def set_refresh_cookie(response, token_data):
    refresh_token = create_refresh_token(token_data)
    max_age = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=max_age,
    )
