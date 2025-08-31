from abc import ABC, abstractmethod
from base64 import b85decode, b85encode
from dataclasses import asdict, dataclass
from itertools import batched, islice
from os import urandom
from pathlib import Path
from typing import Self

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from orjson import dumps, loads


@dataclass(frozen=True, slots=True)
class Key(ABC):
    private: bytes
    public: bytes
    algorithm: str

    @property
    def public_key(self: Self) -> str:
        return b85encode(self.public).decode()

    @staticmethod
    @abstractmethod
    def generate(algorithm: str) -> "Key":
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def from_file(
        path: Path,
        password: str,
    ) -> "Key":
        raise NotImplementedError

    @staticmethod
    def data_from_file(
        path: Path,
        password: str,
    ) -> tuple[bytes, bytes, str]:
        with path.open("r") as file:
            lines = file.readlines()
        encrypted_private_key = EncryptedKey.from_str(
            "".join(islice(lines, 1, len(lines) - 1)).replace("\n", ""),
        )
        return encrypted_private_key.to_key_data(password)

    @abstractmethod
    def to_file(
        self: Self,
        path: Path,
        password: str,
        padding_size: int,
    ) -> None:
        row_len = 128
        encrypted_key = EncryptedKey.from_key(self, password, padding_size)

        begin_phrase = "BEGIN ENCRYPTED KEYS"
        begin_suffix = "-" * ((row_len - len(begin_phrase)) // 2 - 1)
        end_phrase = "END ENCRYPTED KEYS"
        end_suffix = "-" * ((row_len - len(end_phrase)) // 2 - 1)

        data = "\n".join(
            (
                f"{begin_suffix} {begin_phrase} {begin_suffix}",
                *(
                    "".join(batch)
                    for batch in batched(
                        encrypted_key.to_str(),
                        row_len,
                        strict=False,
                    )
                ),
                f"{end_suffix} {end_phrase} {end_suffix}",
            ),
        )

        with path.open("w") as file:
            file.write(data)


@dataclass(frozen=True, slots=True)
class EncryptedKey:
    private: bytes
    public: bytes
    algorithm: bytes
    kdf_salt: bytes
    private_aead_salt: bytes
    public_aead_salt: bytes
    padding: bytes

    @staticmethod
    def _get_secure_password(
        password: str,
        salt: bytes | None = None,
    ) -> tuple[bytes, bytes]:
        kdf_salt = salt or urandom(16)
        secure_password = Argon2id(
            salt=kdf_salt,
            length=32,
            iterations=8,
            lanes=8,
            memory_cost=256 * 1024,
        ).derive(password.encode())
        return secure_password, kdf_salt

    @staticmethod
    def _encrypt(data: bytes, secure_password: bytes) -> tuple[bytes, bytes]:
        salt = urandom(12)
        data = ChaCha20Poly1305(secure_password).encrypt(salt, data, None)
        return data, salt

    @staticmethod
    def _decrypt(data: bytes, secure_password: bytes, salt: bytes) -> bytes:
        return ChaCha20Poly1305(secure_password).decrypt(salt, data, None)

    @staticmethod
    def from_key(
        key: Key,
        password: str,
        padding_size: int,
    ) -> "EncryptedKey":
        secure_password, kdf_salt = EncryptedKey._get_secure_password(password)
        private, private_aead_salt = EncryptedKey._encrypt(
            key.private,
            secure_password,
        )
        public, public_aead_salt = EncryptedKey._encrypt(
            key.public,
            secure_password,
        )
        algorithm = key.algorithm.encode()
        padding = urandom(padding_size)
        return EncryptedKey(
            private=private,
            public=public,
            algorithm=algorithm,
            kdf_salt=kdf_salt,
            private_aead_salt=private_aead_salt,
            public_aead_salt=public_aead_salt,
            padding=padding,
        )

    def to_key_data(self: Self, password: str) -> tuple[bytes, bytes, str]:
        secure_password, _ = EncryptedKey._get_secure_password(
            password,
            self.kdf_salt,
        )
        return (
            EncryptedKey._decrypt(
                self.private,
                secure_password,
                self.private_aead_salt,
            ),
            EncryptedKey._decrypt(self.public, secure_password, self.public_aead_salt),
            self.algorithm.decode(),
        )

    def to_bytes(self: Self) -> bytes:
        return b85encode(
            dumps({k: b85encode(v).decode() for k, v in asdict(self).items()}),
        )

    def to_str(self: Self) -> str:
        return self.to_bytes().decode()

    @staticmethod
    def from_str(
        encoded_data: str,
    ) -> "EncryptedKey":
        data = loads(b85decode(encoded_data))
        return EncryptedKey(
            private=b85decode(data["private"]),
            public=b85decode(data["public"]),
            algorithm=b85decode(data["algorithm"]),
            kdf_salt=b85decode(data["kdf_salt"]),
            private_aead_salt=b85decode(data["private_aead_salt"]),
            public_aead_salt=b85decode(data["public_aead_salt"]),
            padding=b85decode(data["padding"]),
        )
