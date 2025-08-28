from base64 import b85decode, b85encode
from contextlib import suppress

from secure.kem import generate_kem_keypair
from secure.signature import generate_dsa_keypair
from settings.storage import Storage


class KeysMixin:
    @staticmethod
    def get_dsa_private_key() -> bytes:
        with suppress(KeyError):
            return b85decode(Storage[str].get_value("dsa_private_key"))

        private_key, public_key = generate_dsa_keypair()
        Storage[str].set_value("dsa_private_key", b85encode(private_key).decode())
        Storage[str].set_value("dsa_public_key", b85encode(public_key).decode())
        return private_key

    @staticmethod
    def get_dsa_public_key() -> str:
        with suppress(KeyError):
            return Storage[str].get_value("dsa_public_key")

        private_key, public_key = generate_dsa_keypair()
        Storage[str].set_value("dsa_private_key", b85encode(private_key).decode())
        return Storage[str].set_value("dsa_public_key", b85encode(public_key).decode())

    @staticmethod
    def get_kem_private_key() -> bytes:
        with suppress(KeyError):
            return b85decode(Storage[str].get_value("kem_private_key"))

        private_key, public_key = generate_kem_keypair()
        Storage[str].set_value("kem_private_key", b85encode(private_key).decode())
        Storage[str].set_value("kem_public_key", b85encode(public_key).decode())
        return private_key

    @staticmethod
    def get_kem_public_key() -> str:
        with suppress(KeyError):
            return Storage[str].get_value("kem_public_key")

        private_key, public_key = generate_kem_keypair()
        Storage[str].set_value("kem_private_key", b85encode(private_key).decode())
        return Storage[str].set_value("kem_public_key", b85encode(public_key).decode())
