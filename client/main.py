from gui.app import Messenger
from net.chat import WebSocketClient


def main() -> None:
    websocket = WebSocketClient()
    websocket.start()
    queue_send, queue_receive = websocket.get_queues()

    Messenger(1280, 720, queue_send, queue_receive).run()


if __name__ == "__main__":
    main()
