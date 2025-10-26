from os import environ
from pathlib import Path
from models.summarize import summarizer

# environ["OQS_INSTALL_PATH"] = str(
#     Path(__file__).resolve().parent.parent / "libs" / "oqs",
# )

from time import sleep

from gui.app import Messenger
from net.chat import WebSocketClient, get_all_chats


def main() -> None:
    # password = SignIn().password

    websocket = WebSocketClient()
    websocket.start()
    queue_send, queue_receive = websocket.get_queues()
    sleep(1)

    get_all_chats()

    Messenger(1280, 720, queue_send, queue_receive, websocket.stop).run()

print(summarizer("ыта: привет. у меня родился сын. удч: привет. я рада за тебя. а сколько ему лет? ыта: ты тупая?"))
if __name__ == "__main__":
    main()
