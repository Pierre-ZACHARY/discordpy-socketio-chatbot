import asyncio
import datetime
import json
import os
import signal
import uuid
from typing import Union

import discord
import websockets as websockets
from discord import CategoryChannel, TextChannel, Message
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")

websites = {}
uid_channels = {}
keyDict = {}
websockets_todo_setname = {}
websites["CHANNEL_ID"] = os.getenv("CHANNEL_ID")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")


@bot.command()
async def ping(ctx: discord.ext.commands.Context):
    await ctx.send("pong")


@bot.command()
async def clearall(ctx: discord.ext.commands.Context):
    for website, wib in websites.items():
        channel: CategoryChannel = bot.get_channel(int(wib))
        for text_channel in channel.channels:
            await text_channel.delete()


dont_delete = []


@bot.command()
async def disable(ctx: discord.ext.commands.Context):
    dont_delete.append(ctx.channel.id)
    msg: discord.Message = ctx.message
    await msg.add_reaction("✅")


connected = {}


@bot.event
async def on_message(message: discord.message):
    if message.author.id != bot.user.id:
        await bot.process_commands(message)
        channel_id = message.channel.id
        if channel_id in connected:
            websocket = connected[channel_id]
            await websocket.send(json.dumps({"type": "MESSAGE",
                                             "content": message.content,
                                             "attachments": [str(a) for a in message.attachments],
                                             "author": {
                                                 "name": message.author.nick if message.author.nick is not None else message.author.name,
                                                 "avatar_url": str(message.author.avatar_url)}
                                             }))


@bot.event
async def on_typing(channel: discord.abc.Messageable, user: Union[discord.User, discord.Member],
                    when: datetime.datetime):
    if user.id != bot.user.id:
        channel_id = channel.id
        if channel_id in connected:
            websocket = connected[channel_id]
            await websocket.send(json.dumps({"type": "TYPING_EVENT",
                                             "date": when.time().strftime("%H:%M:%S")}))


async def consumer_handler(websocket, path):
    try:
        while True:
            message = await websocket.recv()
            categorie_id = websites[path.split("/")[-1]]
            message = json.loads(message)
            if "key" not in message:
                continue
            if str(websocket) not in keyDict:
                keyDict[str(websocket)] = message["key"]
            if "set_name" in message:
                websockets_todo_setname[str(websocket)] = message["set_name"]
            if "content" in message and message["content"] != "":
                if message["key"] not in uid_channels:
                    channel = bot.get_channel(int(categorie_id))
                    textchannel = await channel.create_text_channel(str(uuid.uuid1()))
                    uid_channels[message["key"]] = textchannel
                    connected[textchannel.id] = websocket
                else:
                    textchannel = uid_channels[message["key"]]
                if websockets_todo_setname[str(websocket)] is not None:
                    if textchannel.name != websockets_todo_setname[str(websocket)]:
                        try:
                            await asyncio.wait_for(
                                textchannel.edit(name=websockets_todo_setname[str(websocket)], timeout=1))
                        except asyncio.TimeoutError:
                            await textchannel.send("Tried to change channel name to : " + websockets_todo_setname[
                                str(websocket)] + " ( API cap exceeded 2edits/10min )")
                    websockets_todo_setname[str(websocket)] = None

                await textchannel.send(message["content"])
    except websockets.ConnectionClosed as e:
        if str(websocket) in keyDict:
            key = keyDict[str(websocket)]
            if key in uid_channels:
                textchannel: TextChannel = uid_channels[key]
                last_msg: Message = textchannel.last_message
                if last_msg.content != "Info : Websocket closed.":
                    await textchannel.send("Info : Websocket closed.")


if __name__ == "__main__":
    server = websockets.serve(
        consumer_handler,
        host="0.0.0.0",
        port=int(os.environ["PORT"]),
    )
    print("listening on port " + str(int(os.environ["PORT"])))
    loop = asyncio.new_event_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    loop.run_until_complete(asyncio.wait([server, stop], return_when=asyncio.FIRST_COMPLETED))
    bot.run(TOKEN)
