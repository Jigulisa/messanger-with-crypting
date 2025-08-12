from base64 import b85decode, b85encode
from contextlib import suppress

from secure.signature import generate_keypair
from settings.storage import Storage


class KeysMixin:
    @staticmethod
    def get_private_key() -> bytes:
        with suppress(KeyError):
            return b85decode(Storage[str].get_value("private_key"))

        private_key, public_key = generate_keypair()
        Storage[str].set_value("private_key", b85encode(private_key).decode())
        Storage[str].set_value("public_key", b85encode(public_key).decode())
        return private_key

    @staticmethod
    def get_public_key() -> str:
        with suppress(KeyError):
            return Storage[str].get_value("public_key")

        private_key, public_key = generate_keypair()
        Storage[str].set_value("private_key", b85encode(private_key).decode())
        return Storage[str].set_value("public_key", b85encode(public_key).decode())
