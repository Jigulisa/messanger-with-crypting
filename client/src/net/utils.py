from settings import Settings
from os import urandom
from datetime import datetime, UTC
from base64 import b85encode
from secure.signature import sign

def get_auth_headers() -> dict[str, str]:
    nonce = urandom(2048)
    return {
        "X-Timestamp": datetime.now(UTC).isoformat(),
        "X-Public-Key": Settings.get_public_key(),
        "X-Nonce": b85encode(nonce).decode(),
        "X-Signature": sign(nonce, Settings.get_private_key()),
    }