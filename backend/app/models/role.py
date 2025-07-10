from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Role(Base):
    __tablename__ = "roles_mst"

    id: Mapped[int] = mapped_column(
        "role_id",
        Integer,
        primary_key=True,
        unique=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        "role_name",
        String,
        unique=True
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=True
    )


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_inf.id"),
        primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles_mst.role_id"),
        primary_key=True
    )
