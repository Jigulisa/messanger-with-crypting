from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession

from messages.models.repositories import (
    AccessRepository,
    ChatRepository,
    MessageRepository,
)


async def provide_chat_repository(
    db_session: AsyncSession,
) -> ChatRepository:
    return ChatRepository(session=db_session)


async def provide_message_repository(
    db_session: AsyncSession,
) -> MessageRepository:
    return MessageRepository(session=db_session)


async def provide_access_repository(
    db_session: AsyncSession,
) -> AccessRepository:
    return AccessRepository(session=db_session)


dependencies = {
    "chat_repository": Provide(provide_chat_repository),
    "message_repository": Provide(provide_message_repository),
    "access_repository": Provide(provide_access_repository),
}
