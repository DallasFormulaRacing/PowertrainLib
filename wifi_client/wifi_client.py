from wifi import Cell, Scheme
import traceback
import logging

# home network will be the network you want to connect to
# password is the password for that network

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Client:
    def __init__(self, device_id: str, home_network: str, password: str):
        self.device_id = device_id
        self.home_network = home_network
        self.password = password

    def get_wifi_networks(self) -> list:
        try:
            logging.info("Getting wifi networks")
            return Cell.all(self.device_id)
        except Exception as e:
            logging.error(f"Error discovering wifi networks: {e}")
            traceback.print_exc(e)
            return []

    def connect(self) -> bool:

        try:
            logging.info("Attempting to connect to wifi")
            networks = self.get_wifi_networks()

            for network in networks:
                if network.ssid == self.home_network:
                    scheme = Scheme.for_cell(self.device_id, network.ssid, network, self.password)
                    scheme.save()
                    scheme.activate()

                    print(f"Connected to wifi: {network.ssid}")
                    logging.info(f"Connected to wifi: {network.ssid}")
                    return True
        except Exception as e:
            logging.error(f"Error connecting to wifi: {e}")
            traceback.print_exc(e)
            return False


def main():
    client = Client('wlan0', 'home_network_ssid', 'home_network_password')
    client.connect()


if __name__ == '__main__':
    main()
