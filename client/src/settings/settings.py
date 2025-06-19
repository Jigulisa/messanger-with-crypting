from pathlib import Path

from msgspec import DecodeError
from msgspec.toml import decode, encode

from settings.keys import KeysMixin


class Settings(KeysMixin):
    path = Path("./settings.toml")

    @staticmethod
    def check_file() -> None:
        if not Settings.path.exists():
            Settings.path.touch()

    @staticmethod
    def get_value[T](key: str, default: T = None) -> T:
        Settings.check_file()

        with Settings.path.open("rb") as file:
            try:
                data = decode(file.read())
            except DecodeError:
                data = {}

        if key in data:
            return data[key]

        return Settings.set_value(key, default)

    @staticmethod
    def set_value[T](key: str, value: T) -> T:
        Settings.check_file()

        with Settings.path.open("rb") as file:
            try:
                data = decode(file.read())
            except DecodeError:
                data = {}

        data[key] = value

        with Settings.path.open("wb") as file:
            file.write(encode(data))

        return value
