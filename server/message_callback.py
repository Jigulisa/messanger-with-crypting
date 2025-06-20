from base64 import b85decode

from pydantic import ValidationError
from typing import Self
from litestar import WebSocket
from oqs import Signature

from message_struct import PrivateMessage

class MessageCallback:
    def __init__(self: Self, socket: WebSocket) -> None:
        self.socket = socket

    @staticmethod
    def validate(data: bytes) -> PrivateMessage | None:
        try:
            message = PrivateMessage.model_validate_json(data)
        except ValidationError:
            return None
        with Signature("ML-DSA-87") as verifier:
            is_valid = verifier.verify(
                message.model_dump_json(exclude={"signature"}).encode(),
                b85decode(message.signature),
                b85decode(message.author),
            )
        return message if is_valid else None

    async def __call__(self: Self, data: bytes) -> None:
        message = self.validate(data)
        if message is None:
            return
        if self.socket.auth in {message.recieve_id, message.author}:
            await self.socket.send_data(message.model_dump_json())