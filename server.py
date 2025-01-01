import asyncio

from websockets.server import serve
from websockets.exceptions import ConnectionClosed
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
clients = set()


async def read_card():
    while True:
        _, text = reader.read()
        if text:
            await broadcast(text)
        await asyncio.sleep(1)


async def send_message(websocket, message):
    try:
        await websocket.send(message)
    except ConnectionClosed:
        pass


async def broadcast(message):
    tasks = [send_message(websocket, message) for websocket in clients]
    await asyncio.gather(*tasks, return_exceptions=True)


async def handler(websocket):
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)


async def main():
    server = await serve(handler, port=8765)
    print("Websocket server started")

    await asyncio.gather(read_card(), server.wait_closed())


if __name__ == "__main__":
    asyncio.run(main())
