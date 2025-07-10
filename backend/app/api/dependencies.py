from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastcrud.exceptions.http_exceptions import ForbiddenException, UnauthorizedException

from app.core.database import async_get_db
from app.services.auth import oauth2_scheme, verify_token
from app.schemas.auth import CurrentUser


SessionDep = Annotated[AsyncSession, Depends(async_get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(token: TokenDep) -> CurrentUser:
    user = verify_token(token)
    if user is None:
        raise UnauthorizedException()
    return user


CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]


async def has_admin_role(user: CurrentUserDep) -> CurrentUser:
    admin_role_name = "admin"
    if admin_role_name in user["roles"]:
        return user
    raise ForbiddenException()


async def has_vendor_role(user: CurrentUserDep) -> CurrentUser:
    vendor_role_name = "vendor"
    if vendor_role_name in user["roles"]:
        return user
    raise ForbiddenException()


AdminRoleDep = Annotated[CurrentUser, Depends(has_admin_role)]
VendorRoleDep = Annotated[CurrentUser, Depends(has_vendor_role)]
