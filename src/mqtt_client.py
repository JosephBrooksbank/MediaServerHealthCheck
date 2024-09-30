import atexit

from paho.mqtt import client as paho_client
from paho.mqtt.client import Client, MQTTMessage
import random
from database import Database
from typing import Any

broker = 'mainsail.local'
port = 1883
topic = "test"
client_id = f'subscribe-{random.randint(0, 1000)}'


def connect_mqtt():
    client = paho_client.Client(paho_client.CallbackAPIVersion.VERSION2)

    def on_connect(client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        client.subscribe(topic)

    def on_disconnect(client, userdata, disconnect_flags, rc, properties):
        print(f"Disconnected with result code {rc}")
        if rc != 0:
            print("Unexpected disconnection.")
            try:
                client.reconnect()
            except Exception as e:
                print(f"Reconnection failed: {e}")

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(broker, port)
    return client


def on_mqtt_message(client: Client, userdata: Any, message: MQTTMessage):
    message_text = str(message.payload.decode('utf-8'))
    print(f"Received message {message_text}")
    if message_text == 'Alive!':
        with Database() as db:
            db.record_timestamp(message_text)


class MqttClient:

    def __enter__(self):
        self.paho_client = connect_mqtt()
        self.paho_client.on_message = on_mqtt_message
        self.paho_client.subscribe(topic)
        self.paho_client.loop_start()
        atexit.register(self.close_mqtt)
        return self

    def close_mqtt(self):
        print("Closing MQTT")
        self.paho_client.loop_stop()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_mqtt()
        return False
