from base64 import b85encode
from pathlib import Path
from typing import Self, override

from oqs import Signature

from secure.core import Key


class SigKey(Key):
    @override
    @staticmethod
    def generate(algorithm: str) -> "SigKey":
        with Signature(algorithm) as sig:
            public = sig.generate_keypair()
            private = sig.export_secret_key()
            return SigKey(private=private, public=public, algorithm=algorithm)

    @override
    @staticmethod
    def from_file(
        path: Path,
        password: str,
    ) -> "SigKey":
        private, public, algorithm = Key.data_from_file(path, password)
        return SigKey(private=private, public=public, algorithm=algorithm)

    @override
    def to_file(
        self: Self,
        path: Path,
        password: str,
        padding_size: int = 40,
    ) -> None:
        return super().to_file(path, password, padding_size)

    def sign(self: Self, data: bytes) -> str:
        with Signature(self.algorithm, self.private) as sig:
            return b85encode(sig.sign(data)).decode()

    def verify(self: Self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        with Signature(self.algorithm) as verifier:
            return verifier.verify(message, signature, public_key)
