import random
from dotenv import dotenv_values
import sqlite3
import atexit

health_checker = None
config = dotenv_values(".env", encoding="utf-8")
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

import discord

from paho.mqtt import client as mqtt_client

broker = 'mainsail.local'
port = 1883
topic = "test"
client_id = f'subscribe-{random.randint(0,1000)}'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')



def on_mqtt_message(client, userdata, message):
    message_text =  str(message.payload.decode("utf-8"))
    print(message.topic + " " + str(message.payload))
    # if message_text == "Alive!":
    #     cursor.execute("INSERT INTO healthcheck (status, timestamp) VALUES (?, ?)", (message_text, message.timestamp))



def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        client.subscribe(topic)
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def run():
    client = connect_mqtt()
    client.subscribe(topic)
    client.on_mqtt_message = on_mqtt_message
    client.loop_start()
    return client

def on_exit():
    connection.close()
    if health_checker is not None:
        print('Stopping health checker')
        health_checker.loop_stop()

if __name__ == '__main__':
    token = config['DISCORD_TOKEN']
    health_checker = run()
    atexit.register(on_exit)
    # client.run(token)
    while True:
        pass



