from os import environ
from pathlib import Path

environ["OQS_INSTALL_PATH"] = str(
    Path(__file__).resolve().parent.parent / "libs" / "oqs",
)

from time import sleep

from gui.app import Messenger, SignIn
from net.chat import WebSocketClient, get_all_chats
from settings.storage import Storage


def main() -> None:
    password = SignIn().password
    if password is None:
        return
    Storage.password = password

    websocket = WebSocketClient()
    websocket.start()
    queue_send, queue_receive = websocket.get_queues()
    sleep(1)

    get_all_chats()

    Messenger(1280, 720, queue_send, queue_receive, websocket.stop).run()


if __name__ == "__main__":
    main()
