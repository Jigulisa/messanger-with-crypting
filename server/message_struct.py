from datetime import datetime

from pydantic import BaseModel


class PrivateMessage(BaseModel):
    message: str
    sent_time: datetime
    author: str
    receive_id: str
    signature: str


class AllFileNamesModel(BaseModel):
    names: list[str]


class DownloadFileModel(BaseModel):
    data: bytes


class RenameModel(BaseModel):
    message: str


class GetFilePropertiesModel(BaseModel):
    name: str
    load_time: datetime
    size: int
    last_touched: datetime


class DeleteModel(BaseModel):
    message: str
