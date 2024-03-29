from box_client.box_client import Client as BoxClient
from discord_client.discord_client import Client as DiscordClient
from mongo_client.mongo_client import Client as MongoClient
from wifi_client.wifi_client import Client as WifiClient

import logging
import os
from dotenv import load_dotenv
import pandas as pd


class Handler:

    def handler():

        load_dotenv()
        WIFI_PASSWORD = os.getenv('WIFI_PASSWORD')
        WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')

        if not WIFI_PASSWORD or not WEBHOOK_URL:
            logging.error("WIFI_PASSWORD or DISCORD_WEBHOOK is not set")

        wifi_client = WifiClient('device_id', 'home_network', WIFI_PASSWORD)
        discord_client = DiscordClient(WEBHOOK_URL)
        box_client = BoxClient()
        mongo_client = MongoClient('cluster0', 'dfr_sensor_data')

        wifi_networks = wifi_client.get_wifi_networks()

        logging.info("Attempting to connect to wifi")

        if 'NETGEAR76' in wifi_networks:
            logging.info("NETGEAR76 found in wifi networks")

            try:
                wifi_client.connect()
                box_client.send_files()
                discord_client.post_message("File uploaded to Box")
                Handler.mongo_upload_handler(mongo_client)

                discord_client.post_message("Documents inserted into MongoDB")
                logging.info("Documents inserted into MongoDB")
            except Exception as e:
                logging.exception(f"An error occurred: {e}")
                print.traceback(e)
                discord_client.post_message(f"An error occurred: {e}")
                return

        logging.error("Wifi network not found in wifi networks")
        return None

    @staticmethod
    def mongo_upload_handler(mongo_client):
        mongo_client.check_connection()

        ecu_df = pd.read_csv("data/ecu_data/ecu_data.csv")
        ecu_dict = ecu_df.to_dict("records")

        # mongo_client.insert_documents(ecu_dict)
        mongo_client.close_connection()


if __name__ == "__main__":
    handler = Handler()
    handler.handler()
