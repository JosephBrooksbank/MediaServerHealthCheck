from discord_client import start_threaded as discord_start_threaded, start as discord_start
from mqtt_client import MqttClient
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    logging.info("Starting health check")
    with MqttClient() as mqtt_client:
        logging.debug("Mqtt client started")
        # run client in a separate thread
        discord_start()



