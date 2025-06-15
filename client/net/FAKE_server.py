from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from uvicorn import run
from datetime import datetime
from time import sleep
from random import randint
from message_struct import Message

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    client_host = websocket.client.host
    print(f"New connection attempt from {client_host}\nCURRENT TIME: {datetime.now().time()}")
    await websocket.accept()
    try:
        while True:
            msg = Message(message=str(randint(0, 100)), sent_time=datetime.now(), author="alya", chat_id=randint(25, 28), spam=False)
            await websocket.send_text(msg.json())
            print(f"data sent at {datetime.now().time()}")
            sleep(randint(5, 25))
    except WebSocketDisconnect:
        print(f"Client {client_host} disconnected\nCURRENT TIME: {datetime.now().time()}")

if __name__ == "__main__":
    run("FAKE_server:app", host="0.0.0.0", port=8000, reload=True)
