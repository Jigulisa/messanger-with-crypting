from base64 import b85decode, b85encode

from oqs import Signature


class KeysMixin:
    @staticmethod
    def get_private_key() -> str:
        from settings.settings import Settings

        private_key = Settings.get_value("private_key")

        if private_key is not None:
            return private_key

        with Signature("ML-DSA-87") as signer:
            return b85encode(signer.export_secret_key()).decode()

    @staticmethod
    def get_private_key_bytes() -> bytes:
        return b85decode(KeysMixin.get_private_key())
