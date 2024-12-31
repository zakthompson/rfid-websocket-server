import asyncio

from websockets.asyncio.server import serve
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()


async def read_card():
    while True:
        id, text = reader.read()
        if text:
            print(f"Card read: {id} {text}")
        await asyncio.sleep(1)


async def handler(websocket):
    async for message in websocket:
        await websocket.send(message)


async def run_server():
    async with serve(handler, "localhost", 8765) as server:
        await server.serve_forever()


async def main():
    await asyncio.gather(run_server(), read_card())


asyncio.run(main())
