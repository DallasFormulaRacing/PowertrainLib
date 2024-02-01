from box_client.box_client import Client as BoxClient
from discord_client.discord_client import Client as DiscordClient
from mongo_client.mongo_client import Client as MongoClient
from wifi_client.wifi_client import Client as WifiClient


# first search for the wifi network and try to identify the correct one
# if the network is found, then upload the files to box and send a message to discord
# this is the genereal idea of how to, go back into discord_client.py and network_client.py and box_client.py
# and make the necessary changes such as making the functions return a boolean or the correct data type
# then utilize the handler.py file to call the functions and make the necessary changes to the handler.py file


class Handler:

    def handler():
        wifi_client = WifiClient('device_id', 'home_network', 'password')
        discord_client = DiscordClient('webhook_url')
        box_client = BoxClient()
        mongo_client = MongoClient('db_name', 'collection_name')

        if 'NETGEAR76' in wifi_client.get_wifi_networks():

            if wifi_client.connect():
                if mongo_client.check_connection():
                    if mongo_client.insert_documents(list):
                        discord_client.post_message("Documents inserted into MongoDB")
                    else:
                        discord_client.post_message("Error inserting documents into MongoDB")
                    mongo_client.close_connection()

                if box_client.send_file():
                    discord_client.post_message("File uploaded to Box")
                else:
                    discord_client.post_message("Error uploading file to Box")

        # network_client = NetworkClient()
        # discord_client = DiscordClient()
        # box_client = BoxClient()

        # if network_client.get_wifi_networks():

        #     if box_client.send_file():
        #         discord_client.post_message("File uploaded to Box")
        #     else:
        #         discord_client.post_message("Error uploading file to Box")



if __name__ == "__main__":
    handler = Handler()
    handler.handler()
