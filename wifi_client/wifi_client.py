import os
import subprocess
import re
import traceback

'''
This script removes all saved networks to ensure that the specific
network passed is chosen when restarting the wifi adapter

We could try testing if appending to the wpa_supplicant.conf file
works so saved wifi networks can remain
'''


class Client:
    def __init__(self, network_name: str, network_password: str):
        self.network_name = network_name
        self.network_password = network_password

    def scan_for_networks(self) -> list:
        try:
            devices = subprocess.check_output(['sudo', 'iwlist', 'wlan0', 'scan'])
            network_names = devices.decode('utf-8')
            network_names = re.findall(r'ESSID:"(.*?)"', devices)

            return network_names

        except subprocess.CalledProcessError as err:
            traceback.print_exc(err.returncode)
            return []

    def connect_to_network(self):
        found = False

        for network_ssid in self.scan_for_networks():
            print(self.network_name, network_ssid)
            if network_ssid == self.network_name:
                print("Found home network")
                found = True
                break

        if found:
            try:
                network = subprocess.check_output(['wpa_passphrase', self.network_name, self.network_password], stderr=subprocess.STDOUT)
                with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w+") as fp:
                    fp.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\ncountry=US\n")
                    fp.write(network.decode("utf8"))

                subprocess.check_output(["wpa_cli", "-i", "wlan0", "reconfigure"])

            except subprocess.CalledProcessError as err:
                found = False
                traceback.print_exc(err.returncode)
        else:
            print("Could not find network")

        return found


def main():
    name = os.getenv('NETWORK_NAME')
    password = os.getenv('NETWORK_PASSWORD')

    client = Client(name, password)
    print(client.connect_to_network())


if __name__ == "__main__":
    main()
