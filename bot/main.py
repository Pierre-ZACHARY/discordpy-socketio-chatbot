import asyncio
import json
import os
import signal
import uuid

import discord
import websockets as websockets
from discord import CategoryChannel
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")

websites = {}
uid_channels = {}
websites["CHANNEL_ID"] = os.getenv("CHANNEL_ID")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")
    for website, wib in websites.items():
        channel: CategoryChannel = bot.get_channel(int(wib))
        for text_channel in channel.channels:
            await text_channel.delete()


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


connected = {}


@bot.event
async def on_message(message: discord.message):
    if message.author.id != bot.user.id:
        channel_id = message.channel.id
        if channel_id in connected:
            websocket = connected[channel_id]
            await websocket.send(json.dumps({"content": message.content, "attachments": message.attachments,
                                             "author": {"name": message.author.nick if message.author.nick is not None else message.author.name,
                                                        "avatar_url": str(message.author.avatar_url)}}))


async def consumer_handler(websocket, path):
    try:
        while True:
            message = await websocket.recv()
            categorie_id = websites[path.split("/")[-1]]
            message = json.loads(message)
            if websocket not in uid_channels:
                channel = bot.get_channel(int(categorie_id))
                textchannel = await channel.create_text_channel(str(uuid.uuid1()))
                uid_channels[websocket] = textchannel
                connected[textchannel.id] = websocket
            else:
                textchannel = uid_channels[websocket]
            if "set_name" in message:
                await textchannel.edit(name=message["set_name"])
            if message["content"] != "":
                await textchannel.send(message["content"])
    except websockets.ConnectionClosed as e:
        textchannel = uid_channels[websocket]
        connected.pop(textchannel.id)
        uid_channels.pop(websocket)
        await textchannel.send("Websocket closed, this channel will be deleted in 10 minutes.")
        await asyncio.sleep(600)
        await textchannel.delete()


if __name__ == "__main__":
    server = websockets.serve(
        consumer_handler,
        host="0.0.0.0",
        port=int(os.environ["PORT"]),
    )
    loop = asyncio.new_event_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    loop.run_until_complete(asyncio.wait([server, stop], return_when=asyncio.FIRST_COMPLETED))
    stop_bot = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop_bot.set_result, None)
    try:
        loop.run_until_complete(asyncio.wait([bot.run(TOKEN), stop_bot], return_when=asyncio.FIRST_COMPLETED))
    except KeyboardInterrupt:
        loop.run_until_complete(bot.close())
        # cancel all tasks lingering
    finally:
        loop.close()
