from box_client.box_client import Client as BoxClient
from discord_client.discord_client import Client as DiscordClient
from mongo_client.mongo_client import Client as MongoClient
from wifi_client.wifi_client import Client as WifiClient

import os
from dotenv import load_dotenv

# first search for the wifi network and try to identify the correct one
# if the network is found, then upload the files to box and send a message to discord
# this is the genereal idea of how to, go back into discord_client.py and network_client.py and box_client.py
# and make the necessary changes such as making the functions return a boolean or the correct data type
# then utilize the handler.py file to call the functions and make the necessary changes to the handler.py file


class Handler:

    def handler():

        load_dotenv()
        WIFI_PASSWORD = os.getenv('WIFI_PASSWORD')
        WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')

        wifi_client = WifiClient('device_id', 'home_network', WIFI_PASSWORD)
        discord_client = DiscordClient(WEBHOOK_URL)
        box_client = BoxClient()
        mongo_client = MongoClient('cluster0', 'dfr_sensor_data')

        wifi_networks = wifi_client.get_wifi_networks()
        if 'NETGEAR76' not in wifi_networks:
            return

        if not wifi_client.connect():
            return

        if not mongo_client.check_connection():
            discord_client.post_message("Error connecting to MongoDB")
            return

        if not mongo_client.insert_documents():
            discord_client.post_message("Error inserting documents into MongoDB")
            return

        discord_client.post_message("Documents inserted into MongoDB")
        mongo_client.close_connection()

        if not box_client.send_file():
            discord_client.post_message("Error uploading file to Box")
            return

        discord_client.post_message("File uploaded to Box")


if __name__ == "__main__":
    handler = Handler()
    handler.handler()
