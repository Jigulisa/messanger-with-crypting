from base64 import b85decode, b85encode

from oqs import KeyEncapsulation


def generate_kem_keypair() -> tuple[bytes, bytes]:
    with KeyEncapsulation("ML-KEM-1024") as kem:
        public_key = kem.generate_keypair()
        return kem.export_secret_key(), public_key


def encap_secret(public_key: str) -> tuple[str, bytes]:
    with KeyEncapsulation("ML-KEM-1024") as kem:
        ciphertext, secret = kem.encap_secret(b85decode(public_key))
    return b85encode(ciphertext).decode(), secret


def decap_secret(secret_key: bytes, ciphertext: bytes) -> bytes:
    with KeyEncapsulation("ML-KEM-1024", secret_key) as kem:
        return kem.decap_secret(ciphertext)
