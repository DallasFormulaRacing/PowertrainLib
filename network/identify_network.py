import platform
import subprocess
import requests


class Client:

    # make this return a boolean
    def get_wifi_networks() -> bool:
        try:
            if platform.system().lower() == 'windows':
                networks = subprocess.check_output(
                    ['netsh', 'wlan', 'show', 'network'])
            elif platform.system().lower() == 'darwin':
                networks = subprocess.check_output(
                    ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s'])
            else:
                print("This script is intended for Windows or macOS systems.")
                return

            decoded_nw = networks.decode('ascii')
            print(decoded_nw)
            return decoded_nw

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
