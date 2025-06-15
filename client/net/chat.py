import asyncio
from websockets import connect, ConnectionClosed
from datetime import datetime


class WebSocketClient:
    def __init__(self, url):
        self.url = url

    async def connect(self) -> None:
        self.connection = await connect(self.url)
        print(f"Connected to server\nCURRENT TIME: {datetime.now().time()}")

    async def listen(self):
        try:
            async for data in self.connection:
                print(f"Received message: {data}\nCURRENT TIME: {datetime.now().time()}")

        except ConnectionClosed:
            print("Oops, Connection closed")

    async def send(self, message):
        if self.connection:
            await self.connection.send(message)
            print(f"Sent message: {message}\nCURRENT TIME: {datetime.now().time()}")

    async def run(self):
        await self.connect()
        await self.listen()


if __name__ == "__main__":
    uri = "ws://localhost:8000/ws"
    client = WebSocketClient(uri)
    asyncio.run(client.run())
