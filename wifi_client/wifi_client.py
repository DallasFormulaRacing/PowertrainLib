import wifi
from wifi import Cell


class Client:
    def __init__(self, device_id: str):
        self.device_id = device_id

    def connect(self, ssid: str, password: str) -> bool:
        networks = Cell.all(self.device_id)
        for network in networks:
            if network.ssid == ssid:
                scheme = wifi.Scheme.for_cell(self.device_id, network.ssid, network, password)
                scheme.save()
                scheme.activate()

                print(f"Connected to wifi: {network.ssid}")
                return True

        print(f"Could not connect to wifi: {ssid}")
        return False


def main():
    client = Client('wlan0')
    client.connect('ssid', 'password')


if __name__ == '__main__':
    main()
