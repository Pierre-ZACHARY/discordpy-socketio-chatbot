import asyncio
import json
import os

import websockets as websockets
from discord import CategoryChannel
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")

websites = {}
uid_channels = {}
websites["PIERRE_ZACHARY_FR"] = os.getenv("PIERRE_ZACHARY_FR")

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


async def response(websocket, path):
    message = await websocket.recv()
    categorie_id = websites[path.split("/")[-1]]
    message = json.loads(message)
    uid = message["uid"]
    content = message["content"]

    if uid not in uid_channels:
        channel = bot.get_channel(int(categorie_id))
        textchannel = await channel.create_text_channel(uid)
        uid_channels[uid] = textchannel
    else:
        textchannel = uid_channels[uid]

    await textchannel.send(content)
    # answer = f"[{message}]"

    # await websocket.send(answer)   # if client expect `response` then server has to send `response`
    # print(f"[ws server] answer > {answer}")

    # `get_channel()` has to be used after `client.run()`
    # channel = client.get_channel(MY_CHANNEL_ID)  # access to channel

    # await channel.send(f'websockets: {message}')


if __name__ == "__main__":
    print(websites)
    server = websockets.serve(response, '0.0.0.0', '8000')
    asyncio.new_event_loop().run_until_complete(server)
    bot.run(TOKEN)
