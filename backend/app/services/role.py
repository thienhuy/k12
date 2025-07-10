from fastcrud import FastCRUD
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.role import Role, UserRole

crud_role = FastCRUD(Role)
# crud_user_role = FastCRUD(UserRole)


async def create_user_roles(db: AsyncSession, roles: list[int], user_id: int) -> list[int]:
    user_roles = [UserRole(role_id=role_id, user_id=user_id) for role_id in roles]
    db.add_all(user_roles)
    await db.commit()
    return roles


async def get_user_roles(db: AsyncSession, user_id: int) -> list[str]:
    result = await db.execute(
        select(Role.name)
        .select_from(UserRole)
        .join(Role, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user_id)
    )
    return result.scalars().all()
