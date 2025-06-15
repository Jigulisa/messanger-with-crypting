from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    message: str
    sent_time: datetime
    author: str
    chat_id: int
    spam: bool
