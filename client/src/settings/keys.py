from base64 import b85decode, b85encode

from secure.signature import generate_keypair
from settings.file import FileMixin


class KeysMixin:
    @staticmethod
    def get_private_key() -> bytes:
        private_key = FileMixin.get_value("private_key")

        if private_key is not None:
            return b85decode(private_key)

        private_key, public_key = generate_keypair()
        FileMixin.set_value("private_key", b85encode(private_key).decode())
        FileMixin.set_value("public_key", b85encode(public_key).decode())
        return private_key

    @staticmethod
    def get_public_key() -> str:
        public_key = FileMixin.get_value("public_key")

        if public_key is not None:
            return public_key

        private_key, public_key = generate_keypair()
        FileMixin.set_value("private_key", b85encode(private_key).decode())
        return FileMixin.set_value("public_key", b85encode(public_key).decode())
