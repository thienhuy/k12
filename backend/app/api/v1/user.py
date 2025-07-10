from fastapi import APIRouter
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from fastcrud.exceptions.http_exceptions import DuplicateValueException, ForbiddenException

from app.api.dependencies import AdminRoleDep, CurrentUserDep, SessionDep
from app.core.message import ErrorMsg
from app.services.user import crud_user, create_user, get_user
from app.services.role import create_user_roles, get_user_roles
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(tags=["users"])


@router.post("/user", response_model=UserRead, status_code=201)
async def post_user(db: SessionDep, user: UserCreate):
    role_ids = user.roles
    del user.roles
    db_user = await create_user(db=db, user=user)
    await create_user_roles(db=db, roles=role_ids, user_id=db_user.id)
    return db_user


@router.get("/users", response_model=PaginatedListResponse[UserRead])
async def get_users(db: SessionDep, page: int, limit: int, dep: AdminRoleDep):
    users = await crud_user.get_multi(
        db=db,
        offset=compute_offset(page, limit),
        limit=limit,
        schema_to_select=UserRead,
        is_deleted=False,
    )
    return paginated_response(users, page, limit)


@router.get("/current-user", response_model=UserRead)
async def get_current_user(db: SessionDep, current_user: CurrentUserDep):
    user = await get_user(db=db, username=current_user["sub"])
    user["roles"] = current_user["roles"]
    return user


@router.get("/user/{username}", response_model=UserRead)
async def get_user_username(db: SessionDep, username: str, dep: CurrentUserDep):
    user = await get_user(db=db, username=username)
    user["roles"] = await get_user_roles(db=db, user_id=user["id"])
    return user


@router.patch("/user", response_model=None)
async def patch_user(db: SessionDep, user: UserUpdate, current_user: CurrentUserDep):
    db_user = await get_user(db=db, id=user.id)
    if db_user.username != current_user["sub"]:
        raise ForbiddenException()

    if user.email != db_user["email"]:
        if await crud_user.exists(db=db, email=user.email):
            raise DuplicateValueException(ErrorMsg.DUPLICATE_EMAIL)

    if user.username != db_user["username"]:
        if await crud_user.exists(db=db, username=user.username):
            raise DuplicateValueException(ErrorMsg.DUPLICATE_USERNAME)

    await crud_user.update(db=db, object=user, id=user.id)
    return None


@router.delete("/user/{username}", response_model=None)
async def delete_user(db: SessionDep, username: str, current_user: CurrentUserDep):
    if username != current_user["sub"]:
        raise ForbiddenException()
    await crud_user.delete(db=db, username=username)
    return None
