import asyncio
import json
import sys
import uuid

import websockets

uri = 'ws://localhost:8000/CHANNEL_ID'


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
    while True:
        message = await ainput("msg: ")
        print(f"[ws client] message  > {message}", end="")
        await websocket.send(json.dumps({"content": message, "key": "testkey"}))


async def send_message():
    async with websockets.connect(uri) as websocket:
        await asyncio.gather(
            consumer_handler(websocket),
            producer_handler(websocket),
        )


if __name__ == "__main__":
    asyncio.new_event_loop().run_until_complete(send_message())
