from os import urandom

from cryptography.hazmat.primitives.kdf.argon2 import Argon2id


def get_n_bytes_password(password: bytes, n: int) -> tuple[bytes, bytes]:
    salt = urandom(16)
    lanes = 4
    kdf = Argon2id(
        salt=salt,
        length=n,
        iterations=1,
        lanes=lanes,
        memory_cost=lanes * 8 * 1024,
    )
    return kdf.derive(password), salt
