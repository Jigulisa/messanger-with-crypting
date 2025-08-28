from base64 import b85encode
from os import urandom

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


def generate_key() -> str:
    return b85encode(ChaCha20Poly1305.generate_key()).decode()


def encrypt(key: bytes, text: str) -> tuple[str, str]:
    nonce = urandom(12)
    return b85encode(
        ChaCha20Poly1305(key).encrypt(nonce, text.encode(), None),
    ).decode(), b85encode(nonce).decode()


def decrypt(key: bytes, text: bytes, nonce: bytes) -> str:
    return ChaCha20Poly1305(key).decrypt(nonce, text, None).decode()
