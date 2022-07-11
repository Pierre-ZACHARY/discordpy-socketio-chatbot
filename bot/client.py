import asyncio
import json
import sys
import uuid

import websockets

uri = 'ws://localhost:8000/PIERRE_ZACHARY_FR'


async def ainput(string: str) -> str:
    await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s+' '))
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)


async def consumer_handler(websocket):
    async for message in websocket:
        print(f"\r[ws server] message  > {message}")
        print("msg: ", end="")


async def producer_handler(websocket):
    new_uuid = uuid.uuid1()

    while True:
        message = await ainput("msg: ")
        print(f"[ws client] message  > {message}", end="")
        await websocket.send(json.dumps({"uid": str(new_uuid), "content": message}))


async def send_message():
    async with websockets.connect(uri) as websocket:
        await asyncio.gather(
            consumer_handler(websocket),
            producer_handler(websocket),
        )


if __name__ == "__main__":
    asyncio.new_event_loop().run_until_complete(send_message())
