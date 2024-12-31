import asyncio

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
clients = set()


async def read_card():
    while True:
        _, text = reader.read()
        if text:
            broadcast(text)
        await asyncio.sleep(1)


async def send_message(websocket, message):
    try:
        await websocket.send(message)
    except ConnectionClosed:
        pass


def broadcast(message):
    for websocket in clients:
        asyncio.create_task(send_message(websocket, message))


async def handler(websocket):
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)


async def run_server():
    server = await serve(handler, port=8765)
    await server.wait_closed()


async def main():
    await asyncio.gather(run_server(), read_card())


asyncio.run(main())
