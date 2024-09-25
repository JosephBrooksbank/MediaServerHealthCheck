import threading
import dotenv

import discord
from discord.ext import tasks
from database import Database

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

config = dotenv.dotenv_values("../.env", encoding="utf-8")


@client.event
async def on_ready():
    check_health.start()
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello! 2')


sent_status_fail = False


@tasks.loop(seconds=30)
async def check_health():
    print("Checking health")
    with Database() as db:
        time_diff = db.get_latest_alive()
        print(f"Time diff is {time_diff}")
        if time_diff > 30:
            print("Server is down!")
            if not db.get_sent_failure():
                await send_status()
        else:
            db.set_sent_failure(False)


async def send_status():
    channel = client.get_channel(int(config['DISCORD_CHANNEL_ID']))
    if channel:
        await channel.send("@everyone the server is down!")
        with Database() as db:
            db.set_sent_failure(True)


def start_threaded():
    thread = threading.Thread(target=client.run, args=(config['DISCORD_TOKEN'],))
    thread.daemon = True
    thread.start()


def start():
    client.run(config['DISCORD_TOKEN'])
