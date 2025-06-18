from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    message: str
    sent_time: datetime
    author: str
    chat_id: int
    spam: bool
