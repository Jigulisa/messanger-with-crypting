from oqs import KeyEncapsulation


def encap_secret(public_key: bytes) -> tuple[bytes, bytes]:
    with KeyEncapsulation("ML-KEM-1024") as kem:
        return kem.encap_secret(public_key)


def decap_secret(secret_key: bytes, ciphertext: bytes) -> bytes:
    with KeyEncapsulation("ML-KEM-1024", secret_key) as kem:
        return kem.decap_secret(ciphertext)
