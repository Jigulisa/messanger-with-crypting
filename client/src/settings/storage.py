from contextlib import suppress
from pathlib import Path
from typing import Any, overload

from msgspec import DecodeError
from msgspec.toml import decode, encode


class Storage[T: list | dict | str | int | float | bool]:
    base_dir = Path(__file__).resolve().parent.parent.parent
    path = base_dir / "settings.toml"

    @staticmethod
    def check_file() -> None:
        if not Storage.path.exists():
            Storage.path.touch()

    @staticmethod
    def get_data() -> dict[str, Any]:
        Storage.check_file()
        with Storage.path.open("rb") as file, suppress(DecodeError):
            return decode(file.read())
        return {}

    @overload
    @staticmethod
    def get_value(key: str) -> T: ...

    @overload
    @staticmethod
    def get_value(key: str, default: T) -> T: ...

    @staticmethod
    def get_value(key: str, default: T | None = None) -> T:
        data = Storage.get_data()

        if key in data:
            return data[key]

        if default is None:
            raise KeyError

        return Storage.set_value(key, default)

    @staticmethod
    def set_value(key: str, value: T) -> T:
        data = Storage.get_data()

        data[key] = value

        with Storage.path.open("wb") as file:
            file.write(encode(data))

        return value
