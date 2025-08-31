from base64 import b85encode
from os import urandom

from cryptography.hazmat.primitives.kdf.argon2 import Argon2id


def get_n_bytes_password(
    password: bytes,
    n: int,
    salt: bytes | None = None,
) -> tuple[bytes, str]:
    salt = salt or urandom(16)
    kdf = Argon2id(
        salt=salt,
        length=n,
        iterations=8,
        lanes=8,
        memory_cost=256 * 1024,
    )
    return kdf.derive(password), b85encode(salt).decode()
