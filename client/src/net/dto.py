from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class MessageDTO(BaseModel):
    text: str
    salt: str
    sent_time: datetime
    author: str
    chat_id: UUID
    signature: str
    is_spam: bool = Field(exclude=True, default=False)


class AccessChatDTO(BaseModel):
    chat_id: UUID
    chat_name: str | None
    secret: str
    secret_salt: str
    key: str
    key_salt: str
