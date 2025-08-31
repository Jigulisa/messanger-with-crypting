from base64 import b85encode
from datetime import UTC, datetime
from os import urandom

from settings import Settings


def get_auth_headers() -> dict[str, str]:
    nonce = urandom(2048)
    return {
        "X-Timestamp": datetime.now(UTC).isoformat(),
        "X-DSA-Public-Key": Settings.get_sig_key().public_key,
        "X-KEM-Public-Key": Settings.get_kem_key().public_key,
        "X-Nonce": b85encode(nonce).decode(),
        "X-Signature": Settings.get_sig_key().sign(nonce),
    }
