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


class AccessChatDTO(BaseModel):
    chat_id: UUID
    chat_name: str | None
    secret: str
    secret_salt: str
    key: str
    key_salt: str


class CreateChat(BaseModel):
    chat_name: str | None = Field(min_length=1, default=None)
    description: str | None = Field(min_length=1)
    secret: str
    secret_salt: str
    key: str
    key_salt: str


class GrantAccess(BaseModel):
    chat_id: UUID
    user: str
    secret: str
    secret_salt: str
    key: str
    key_salt: str
