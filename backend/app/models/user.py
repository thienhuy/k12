
from uuid import UUID, uuid4
from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.core.mixin import Timestamp, SoftDelete


class User(Base, Timestamp, SoftDelete):
    __tablename__ = "user_inf"

    id: Mapped[int] = mapped_column(
        Integer,
        autoincrement=True,
        primary_key=True,
        unique=True,
        init=False
    )
    uuid: Mapped[UUID] = mapped_column(
        "user_id",
        UUID,
        default_factory=uuid4
    )
    username: Mapped[str] = mapped_column(
        "user_name",
        String(50),
        unique=True,
        index=True,
        default=None,
    )
    email: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        default=None,
    )
    password: Mapped[str] = mapped_column(
        String,
        default=None,
    )
    user_type: Mapped[str] = mapped_column(
        String(1),
        default=None,
    )
    full_name: Mapped[str] = mapped_column(
        String(50),
        default=None,
    )
