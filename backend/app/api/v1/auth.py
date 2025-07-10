from typing import Annotated

from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastcrud.exceptions.http_exceptions import UnauthorizedException

from app.api.dependencies import SessionDep
from app.core.message import ErrorMsg
from app.schemas.auth import Token
from app.services.role import get_user_roles
from app.services.auth import authenticate_user, create_access_token, set_refresh_cookie, verify_token

router = APIRouter(tags=["login"])


@router.post("/login", response_model=Token)
async def login(
    db: SessionDep,
    response: Response,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await authenticate_user(db, form.username, form.password)
    token_data = {"sub": user["username"]}
    token_data["roles"] = await get_user_roles(db=db, user_id=user["id"])
    token = create_access_token(token_data)
    set_refresh_cookie(response, token_data)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
def refresh_access_token(request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
        raise UnauthorizedException(ErrorMsg.MISSING_TOKEN)

    user = verify_token(token)
    if not user:
        raise UnauthorizedException(ErrorMsg.INVALID_TOKEN)

    new_token = create_access_token(user)
    return {"access_token": new_token, "token_type": "bearer"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="refresh_token")
    return {"detail": "Logged out successfully"}
