from base64 import b85decode, b85encode
from pathlib import Path
from typing import Self, override

from oqs import KeyEncapsulation

from secure.aead import encrypt
from secure.core import Key
from secure.kdf import get_n_bytes_password


class KemKey(Key):
    @override
    @staticmethod
    def generate(algorithm: str) -> "KemKey":
        with KeyEncapsulation(algorithm) as kem:
            public = kem.generate_keypair()
            private = kem.export_secret_key()
            return KemKey(private=private, public=public, algorithm=algorithm)

    @override
    @staticmethod
    def from_file(
        path: Path,
        password: str,
    ) -> "KemKey":
        private, public, algorithm = Key.data_from_file(path, password)
        return KemKey(private=private, public=public, algorithm=algorithm)

    @override
    def to_file(
        self: Self,
        path: Path,
        password: str,
        padding_size: int = 5,
    ) -> None:
        return super().to_file(path, password, padding_size)

    def encap_secret(self: Self, public_key: str) -> tuple[str, bytes]:
        with KeyEncapsulation(self.algorithm) as kem:
            ciphertext, secret = kem.encap_secret(b85decode(public_key))
        return b85encode(ciphertext).decode(), secret

    def encap_chat_key(
        self: Self,
        public_key: str,
        chat_key: str,
    ) -> tuple[str, str, str, str]:
        ciphertext, secret = self.encap_secret(public_key)
        password, secret_salt = get_n_bytes_password(secret, 32)
        encrypted_key, key_salt = encrypt(password, chat_key)
        return ciphertext, secret_salt, encrypted_key, key_salt

    def decap_secret(self: Self, ciphertext: str) -> bytes:
        with KeyEncapsulation(self.algorithm, self.private) as kem:
            return kem.decap_secret(b85decode(ciphertext))
