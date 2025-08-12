from http import HTTPStatus

import requests

from settings.server import ServerMixin


def get_file_names() -> list[str] | None:
    response = requests.get(
        ServerMixin.get_server_storage_url("get_file_names/"),
        timeout=10,
    )

    if response.status_code == HTTPStatus.OK:
        return response.json()
    return None


def download_file(name: str) -> bytes | None:
    param = {
        "name": name,
    }
    response = requests.get(
        ServerMixin.get_server_storage_url("download_file/"),
        params=param,
        timeout=10,
    )

    if response.status_code == HTTPStatus.OK:
        return response.content
    return None


def rename(old: str, new: str) -> str:
    param = {"old_name": old, "new_name": new}
    response = requests.post(
        ServerMixin.get_server_storage_url("rename_file/"),
        data=param,
        timeout=10,
    )
    if response.status_code == HTTPStatus.OK:
        return "Done."
    return "Error. Try Again."
