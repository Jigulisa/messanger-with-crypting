from litestar.plugins.sqlalchemy import base
from sqlalchemy.orm import Mapped, mapped_column


class User(base.UUIDv7AuditBase):
    dsa_public_key: Mapped[str] = mapped_column(unique=True)
    kem_public_key: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    personal_data: Mapped[str | None]
