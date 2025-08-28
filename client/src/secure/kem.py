from base64 import b85decode, b85encode

from oqs import KeyEncapsulation

from secure.aead import encrypt
from secure.kdf import get_n_bytes_password


def generate_kem_keypair() -> tuple[bytes, bytes]:
    with KeyEncapsulation("ML-KEM-1024") as kem:
        public_key = kem.generate_keypair()
        return kem.export_secret_key(), public_key


def encap_secret(public_key: str) -> tuple[str, bytes]:
    with KeyEncapsulation("ML-KEM-1024") as kem:
        ciphertext, secret = kem.encap_secret(b85decode(public_key))
    return b85encode(ciphertext).decode(), secret


def decap_secret(ciphertext: str, private_key: bytes) -> bytes:
    with KeyEncapsulation("ML-KEM-1024", private_key) as kem:
        return kem.decap_secret(b85decode(ciphertext))


def encap_chat_key(public_key: str, chat_key: str) -> tuple[str, str, str, str]:
    ciphertext, secret = encap_secret(public_key)
    password, secret_salt = get_n_bytes_password(secret, 32)
    encrypted_key, key_salt = encrypt(password, chat_key)
    return ciphertext, secret_salt, encrypted_key, key_salt
