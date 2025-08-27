from os import environ
from pathlib import Path

environ["OQS_INSTALL_PATH"] = str(
    Path(__file__).resolve().parent.parent / "libs" / "oqs",
)

from gui.app import Messenger, SignIn
from net.chat import WebSocketClient


def main() -> None:
    password = SignIn().password

    websocket = WebSocketClient()
    websocket.start()
    queue_send, queue_receive = websocket.get_queues()

    Messenger(1280, 720, queue_send, queue_receive, websocket.stop).run()


if __name__ == "__main__":
    main()
