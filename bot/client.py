import asyncio
import json
import websockets

uri = 'ws://localhost:8000/PIERRE_ZACHARY_FR'


async def send_message():
    async with websockets.connect(uri) as websocket:
        message = input("msg: ")

        new_uuid = "testuid"

        await websocket.send(json.dumps({"uid": str(new_uuid), "content": message}))
        print(f"[ws client] message  > {message}")



if __name__ == "__main__":
    asyncio.new_event_loop().run_until_complete(send_message())
