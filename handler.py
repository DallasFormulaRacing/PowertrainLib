from box_client.box_client import Client as BoxClient
from discord_client.discord_client import Client as DiscordClient
from mongo_client.mongo_client import Client as MongoClient
from wifi_client.wifi_client import Client as WifiClient

import os
from dotenv import load_dotenv
import json

'''
TODO: wifi code has been rewritten, needs updating here

TODO: only upload new files, not all files
        - mark files that have been uploaded
            (append "_dash_uploaded" or something similar to the end of the uploaded files)
        - Whenever handler is called again after testing days, ignore files that have already renamed
        
TODO: add more descriptive discord webhook message(s)
        - files that are uploaded
        - size of individual files
        - size of all files uploaded
        
TODO: Need to pass a list of file paths to upload into mongo/box

'''

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

        if wifi_client.connect_to_network():

            try:
                box_client.send_files()
                discord_client.post_message("File uploaded to Box")
                mongo_client.check_connection()
                mongo_client.insert_documents()
                mongo_client.close_connection()

                discord_client.post_message("Documents inserted into MongoDB")
            except Exception as e:
                print.traceback(e)
                discord_client.post_message(f"An error occurred: {e}")
                return

        return None


if __name__ == "__main__":
    handler = Handler()
    handler.handler()
