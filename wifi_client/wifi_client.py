import wifi
from wifi import Cell, Scheme
import traceback
import os

# home network will be the network you want to connect to
# password is the password for that network


class Client:
    def __init__(self, device_id: str, home_network: str, password: str):
        self.device_id = device_id
        self.home_network = home_network
        self.password = password

    def get_wifi_networks(self) -> list:
        try:
            return Cell.all("d8:3a:dd:19:9f:a4")
        except:
            traceback.print_exc()
            return []

    def connect(self) -> bool:

        connected = False

        networks = self.get_wifi_networks()

        for network in networks:
            print(network)

        for network in networks:
            print(network.ssid)
            if network.ssid == self.home_network:
                print("Found home network")
                scheme = wifi.Scheme.for_cell(self.device_id, network.ssid, network, self.password)

                try:
                    scheme.save()
                    scheme.activate()

                    print(f"Connected to wifi: {network.ssid}")
                    connected = True

                except wifi.exceptions.ConnectionError as err:
                    traceback.print_exc(err)
                    connected = False

        return connected


def main():
    device_id = os.getenv("DEVICE_ID")
    home_network = os.getenv("NETWORK_SSID")
    password = os.getenv("NETWORK_PASSWORD")
    client = Client(device_id, home_network, password)

    # client.get_wifi_networks()
    print(client.connect())


if __name__ == '__main__':
    main()
