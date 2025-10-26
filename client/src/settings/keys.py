from secure.kem import KemKey
from secure.sig import SigKey
from settings.storage import Storage


class KeysMixin:
    @staticmethod
    def get_sig_key() -> SigKey:
        path = Storage.base_dir / "keys" / "sig_keys.pem"
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            SigKey.generate("ML-DSA-87").to_file(path, Storage.password)
        return SigKey.from_file(path, Storage.password)

    @staticmethod
    def get_kem_key() -> KemKey:
        path = Storage.base_dir / "keys" / "kem_keys.pem"
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            KemKey.generate("ML-KEM-1024").to_file(path, Storage.password)
        return KemKey.from_file(path, Storage.password)
