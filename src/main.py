from discord_client import start_threaded as discord_start_threaded, start as discord_start
from mqtt_client import MqttClient

if __name__ == '__main__':
    with MqttClient() as mqtt_client:
        # run client in a separate thread
        discord_start()



