from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class MessageDTO(BaseModel):
    text: str
    sent_time: datetime
    author: str
    chat_id: UUID
    signature: str


class CreateChat(BaseModel):
    description: str | None = Field(min_length=1)


class GrantAccess(BaseModel):
    chat_id: UUID
    user: str
    key: str
