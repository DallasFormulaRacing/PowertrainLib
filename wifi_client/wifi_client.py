import wifi
from wifi import Cell, Scheme
import traceback

# home network will be the network you want to connect to
# password is the password for that network


class Client:
    def __init__(self, device_id: str, home_network: str, password: str):
        self.device_id = device_id
        self.home_network = home_network
        self.password = password

    def get_wifi_networks(self) -> list:
        try:
            return Cell.all(self.device_id)
        except:
            traceback.print_exc()
            return []

    def connect(self) -> bool:

        try:
            networks = self.get_wifi_networks()

            for network in networks:
                if network.ssid == self.home_network:
                    scheme = wifi.Scheme.for_cell(self.device_id, network.ssid, network, self.password)
                    scheme.save()
                    scheme.activate()

                    print(f"Connected to wifi: {network.ssid}")
                    return True
        except:
            traceback.print_exc()
            return False


def main():
    client = Client('wlan0', 'home_network_ssid', 'home_network_password')
    client.connect()


if __name__ == '__main__':
    main()
