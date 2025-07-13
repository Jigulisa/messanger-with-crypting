from datetime import datetime

from pydantic import BaseModel


class PrivateMessage(BaseModel):
    message: str
    sent_time: datetime
    author: str
    recieve_id: str
    signature: str
