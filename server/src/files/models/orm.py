from litestar.plugins.sqlalchemy import base
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from users.models.orm import User


class File(base.UUIDv7AuditBase):
    name: Mapped[str]
    data: Mapped[bytes]

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    owner: Mapped[User] = relationship()
