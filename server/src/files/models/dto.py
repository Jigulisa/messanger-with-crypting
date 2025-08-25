from datetime import datetime

from pydantic import BaseModel


class FileProperties(BaseModel):
    name: str
    owner: str
    size: int
    created_at: datetime
    updated_at: datetime
