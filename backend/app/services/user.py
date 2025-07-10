from typing import Any
from fastcrud import FastCRUD
from fastcrud.exceptions.http_exceptions import DuplicateValueException, NotFoundException
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.user import User
from app.core.message import ErrorMsg
from app.core.utils import get_password_hash
from app.schemas.user import UserRead

crud_user = FastCRUD(User)


async def get_user(db: AsyncSession, **kwargs: Any):
    user = await crud_user.get(
        db=db,
        schema_to_select=UserRead,
        is_deleted=False,
        **kwargs,
    )
    if user is None:
        raise NotFoundException()
    return user


async def create_user(db: AsyncSession, user: User):
    if await crud_user.exists(db=db, email=user.email):
        raise DuplicateValueException(ErrorMsg.DUPLICATE_EMAIL)

    if await crud_user.exists(db=db, username=user.username):
        raise DuplicateValueException(ErrorMsg.DUPLICATE_USERNAME)

    user.password = get_password_hash(user.password)
    return await crud_user.create(db, user)
