from datetime import datetime

from litestar.plugins.sqlalchemy import base
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from users.models.orm import User


class Chat(base.UUIDv7AuditBase):
    description: Mapped[str | None]

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    owner: Mapped[User] = relationship(lazy="joined")


class Message(base.UUIDv7AuditBase):
    text: Mapped[str]
    salt: Mapped[str]
    sent_time: Mapped[datetime]

    author_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    author: Mapped[User] = relationship(lazy="joined")

    chat_id: Mapped[UUID] = mapped_column(ForeignKey("chat.id"))
    chat: Mapped[Chat] = relationship(lazy="joined")

    signature: Mapped[str]


class Access(base.UUIDv7AuditBase):
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(lazy="joined")

    chat_id: Mapped[UUID] = mapped_column(ForeignKey("chat.id"))
    chat: Mapped[Chat] = relationship(lazy="joined")

    chat_name: Mapped[str | None]

    role: Mapped[str]

    secret: Mapped[str]
    secret_salt: Mapped[str]
    key: Mapped[str]
    key_salt: Mapped[str]
