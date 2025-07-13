from base64 import b85decode, b85encode

from secure.signature import generate_keypair


class KeysMixin:
    @staticmethod
    def get_private_key() -> bytes:
        from settings.settings import Settings

        private_key = Settings.get_value("private_key")

        if private_key is not None:
            return b85decode(private_key)

        private_key, public_key = generate_keypair()
        Settings.set_value("private_key", b85encode(private_key).decode())
        Settings.set_value("public_key", b85encode(public_key).decode())
        return private_key

    @staticmethod
    def get_public_key() -> str:
        from settings.settings import Settings

        public_key = Settings.get_value("public_key")

        if public_key is not None:
            return public_key

        private_key, public_key = generate_keypair()
        Settings.set_value("private_key", b85encode(private_key).decode())
        return Settings.set_value("public_key", b85encode(public_key).decode())
