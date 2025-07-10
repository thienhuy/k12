from fastapi import APIRouter
from fastcrud.paginated import PaginatedListResponse, paginated_response

from app.api.dependencies import SessionDep
from app.services.role import crud_role
from app.schemas.role import RoleRead

router = APIRouter(tags=["role-master"])


@router.get( "/role-mst", response_model=PaginatedListResponse[RoleRead])
async def get_roles(db: SessionDep):
    roles = await crud_role.get_multi(db=db, limit=None)
    return paginated_response(roles, 0, 0)
