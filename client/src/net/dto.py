from datetime import datetime

from pydantic import BaseModel, Field


class MessageDTO(BaseModel):
    text: str
    sent_time: datetime
    author: str
    chat_id: str
    signature: str
    is_spam: bool = Field(exclude=True, default=False)
