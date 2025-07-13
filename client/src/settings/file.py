from pathlib import Path

from msgspec import DecodeError
from msgspec.toml import decode, encode


class FileMixin:
    path = Path("./settings.toml")

    @staticmethod
    def check_file() -> None:
        if not FileMixin.path.exists():
            FileMixin.path.touch()

    @staticmethod
    def get_value[T](key: str, default: T = None) -> T:
        FileMixin.check_file()

        with FileMixin.path.open("rb") as file:
            try:
                data = decode(file.read())
            except DecodeError:
                data = {}

        if key in data:
            return data[key]

        return default if default is None else FileMixin.set_value(key, default)

    @staticmethod
    def set_value[T](key: str, value: T) -> T:
        FileMixin.check_file()

        with FileMixin.path.open("rb") as file:
            try:
                data = decode(file.read())
            except DecodeError:
                data = {}

        data[key] = value

        with FileMixin.path.open("wb") as file:
            file.write(encode(data))

        return value
