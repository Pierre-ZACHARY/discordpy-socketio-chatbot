# you can edit the channel name
import asyncio
import json
import sys
import uuid

import websockets

uri = 'ws://chatbot.pierre-zachary.fr/CHANNEL_ID'


async def ainput(string: str) -> str:
    await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s+' '))
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)


async def consumer_handler(websocket):
    async for message in websocket:
        print(f"\r[ws server] message  > {message}")
        print("set_name: ", end="")


async def producer_handler(websocket):
    await websocket.send(json.dumps({"content": ""})) # open a new channel
    while True:
        name = await ainput("set_name: ")
        print(f"[ws client] set_name  > {name}", end="")
        await websocket.send(json.dumps({"content": "", "set_name": name}))


async def send_message():
    async with websockets.connect(uri) as websocket:
        await asyncio.gather(
            consumer_handler(websocket),
            producer_handler(websocket),
        )


if __name__ == "__main__":
    asyncio.new_event_loop().run_until_complete(send_message())
