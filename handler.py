from box_client.box_client import Client as BoxClient
from discord_client.discord_client import Client as DiscordClient
from network.identify_network import Client as NetworkClient


# first search for the wifi network and try to identify the correct one
# if the network is found, then upload the files to box and send a message to discord
# this is the genereal idea of how to, go back into discord_client.py and network_client.py and box_client.py
# and make the necessary changes such as making the functions return a boolean or the correct data type
# then utilize the handler.py file to call the functions and make the necessary changes to the handler.py file


class Handler:

    def handler():
        network_client = NetworkClient()
        discord_client = DiscordClient()
        box_client = BoxClient()

        if network_client.get_wifi_networks():

            if box_client.send_file():
                discord_client.post_message("File uploaded to Box")
            else:
                discord_client.post_message("Error uploading file to Box")


if __name__ == "__main__":
    handler = Handler()
    handler.handler()
