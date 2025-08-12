from datetime import datetime

from pydantic import BaseModel, Field


class PrivateMessage(BaseModel):
    message: str
    sent_time: datetime
    author: str
    receive_id: str
    signature: str
    is_spam: bool = Field(exclude=True, default=False)
