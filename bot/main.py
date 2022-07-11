import os
from discord.ext import commands
import socketio

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")

websites = {}

for k, v in sorted(os.environ.items()):
    if k != "DISCORD_TOKEN":
        # New website
        websites[k] = v

# create a Socket.IO server
sio = socketio.AsyncServer()

# wrap with ASGI application
app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ, auth):
    print('connect ', sid, environ, auth)


@sio.event
async def disconnect(sid):
    print('disconnect ', sid)


@sio.on('*')
async def catch_all(event, sid, data):
    print('event ', sid, event, data)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


if __name__ == "__main__":
    bot.run(TOKEN)
