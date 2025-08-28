from litestar.plugins.sqlalchemy import repository

from messages.models.orm import Access, Chat, Message


class ChatRepository(repository.SQLAlchemyAsyncRepository[Chat]):
    model_type = Chat


class MessageRepository(repository.SQLAlchemyAsyncRepository[Message]):
    model_type = Message


class AccessRepository(repository.SQLAlchemyAsyncRepository[Access]):
    model_type = Access
