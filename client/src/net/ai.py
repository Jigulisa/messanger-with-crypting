import tarfile
from http import HTTPStatus
from io import BytesIO

from requests import RequestException, get

from net.utils import get_auth_headers
from settings import Settings
from settings.storage import Storage


def get_spam_tracker_model() -> None:
    try:
        response = get(
            Settings.get_server_ai_url("/spam-tracker"),
            timeout=10,
            headers=get_auth_headers(),
        )
    except RequestException:
        return

    if response.status_code != HTTPStatus.OK:
        return

    with tarfile.open(fileobj=BytesIO(response.content), mode="r:xz") as file:
        file.extractall(Storage.base_dir / ".cache/", filter="data")


def get_summarization_model() -> None:
    try:
        response = get(
            Settings.get_server_ai_url("/summarization"),
            timeout=10,
            headers=get_auth_headers(),
        )
    except RequestException:
        return

    if response.status_code != HTTPStatus.OK:
        return

    with tarfile.open(fileobj=BytesIO(response.content), mode="r:xz") as file:
        file.extractall(Storage.base_dir / ".cache/", filter="data")


def get_auto_answer_model() -> None:
    try:
        response = get(
            Settings.get_server_ai_url("/auto_answer"),
            timeout=10,
            headers=get_auth_headers(),
        )
    except RequestException:
        return

    if response.status_code != HTTPStatus.OK:
        return

    with tarfile.open(fileobj=BytesIO(response.content), mode="r:xz") as file:
        file.extractall(Storage.base_dir / ".cache/", filter="data")
