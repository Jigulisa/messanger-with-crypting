from http import HTTPStatus

from requests import RequestException, delete, get, post

from net.utils import get_auth_headers
from settings.server import ServerMixin


def get_file_names() -> list[str] | None:
    try:
        response = get(
            ServerMixin.get_server_storage_url("names"),
            timeout=10,
            headers=get_auth_headers(),
        )
    except RequestException:
        return None

    if response.status_code == HTTPStatus.OK:
        return response.json()

    return None


def download_file(name: str) -> bytes | None:
    param = {"name": name}

    try:
        response = get(
            ServerMixin.get_server_storage_url("download"),
            params=param,
            timeout=10,
            headers=get_auth_headers(),
        )
    except RequestException:
        return None

    if response.status_code == HTTPStatus.OK:
        return response.content
    return None


def rename(old: str, new: str) -> str:
    param = {"old": old, "new": new}

    try:
        response = post(
            ServerMixin.get_server_storage_url("rename"),
            data=param,
            timeout=10,
            headers=get_auth_headers(),
        )
    except RequestException:
        return "Error. Try Again."

    if response.status_code == HTTPStatus.OK:
        return "Done."

    return "Error. Try Again."


def get_file_properties(name: str) -> str:
    param = {"name": name}

    try:
        response = get(
            ServerMixin.get_server_storage_url("properties/"),
            params=param,
            timeout=10,
            headers=get_auth_headers(),
        )
    except RequestException:
        return "Error. Try Again."

    if response.status_code == HTTPStatus.OK:
        return response.json()

    return "Error. Try Again."


def delete_file(name: str) -> str:
    param = {"name": name}
    try:
        response = delete(
            ServerMixin.get_server_storage_url("delete"),
            data=param,
            timeout=10,
            headers=get_auth_headers(),
        )
    except RequestException:
        return "Error. Try Again."

    if response.status_code == HTTPStatus.OK:
        return "Done. File deleted."

    return "Error. Try Again."
