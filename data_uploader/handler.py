from data_uploader.box_client.box_client import Client as BoxClient
from data_uploader.discord_client.discord_client import Client as DiscordClient
from data_uploader.discord_client.messages import Messages as discord_messages
from data_uploader.mongo_client.mongo_client import Client as MongoClient
from data_uploader.wifi_client.wifi_client import Client as WifiClient


import os
from dotenv import load_dotenv
import json


config = json.load(
    open('512311_xk3jq6ao_config.json')
)


class Handler:

    def handler():

        load_dotenv()
        NETWORK_NAME = os.getenv('NETWORK_NAME')
        WIFI_PASSWORD = os.getenv('NETWORK_PASSWORD')
        WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')

        wifi_client = WifiClient(NETWORK_NAME, WIFI_PASSWORD)
        discord_client = DiscordClient(WEBHOOK_URL)
        box_client = BoxClient(config['boxAppSettings']['clientID'], config['boxAppSettings']['clientSecret'], config['enterpriseID'], config['appAuth']['publicKeyID'],
                               config['appAuth']['privateKey'], config['boxAppSettings']['appAuth']['passphrase'], config['file_path'], config['folder_id'])
        mongo_client = MongoClient('cluster0', 'dfr_sensor_data')

        files_for_upload = []

        if wifi_client.connect_to_network():

            discord_client.post_message(discord_messages.WIFI_SUCCESS_MESSAGE)

            try:
                files_for_upload = box_client.discover_files()
                box_client.send_files(files_for_upload)

                discord_client.post_message(discord_messages.BOX_SUCCESS_MESSAGE)

                mongo_client.check_connection()
                mongo_client.insert_documents(files_for_upload)
                discord_client.post_message(discord_messages.MONGO_SUCCESS_MESSAGE)
                mongo_client.close_connection()
                discord_client.post_message(discord_messages.MONGO_CLOSE_MESSAGE)

                discord_client.post_message("Documents inserted into MongoDB")
            except Exception as e:
                print.traceback(e)
                discord_client.post_message(f"An error occurred: {e}")
                return

        discord_client.post_message(discord_messages.WIFI_ERROR_MESSAGE)

        return None


if __name__ == "__main__":
    handler = Handler()
    handler.handler()
