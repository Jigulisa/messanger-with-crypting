from base64 import b85encode

from oqs import Signature


def verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
    with Signature("ML-DSA-87") as verifier:
        return verifier.verify(message, signature, public_key)


def sign(message: bytes, private_key: bytes) -> str:
    with Signature("ML-DSA-87", private_key) as signer:
        return b85encode(signer.sign(message)).decode()


def generate_dsa_keypair() -> tuple[bytes, bytes]:
    with Signature("ML-DSA-87") as generator:
        public_key = generator.generate_keypair()
        return generator.export_secret_key(), public_key
