from datetime import datetime

from pydantic import BaseModel


class SentPrivateMessage(BaseModel):
    message: str
    sent_time: datetime
    author: str
    recieve_id: str
    signature: str


class ReceivedPrivateMessage(BaseModel):
    message: str
    sent_time: datetime
    author: str
    recieve_id: str
    signature: str
    spam: bool
