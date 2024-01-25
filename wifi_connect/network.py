import platform
import subprocess
import requests

def get_wifi_networks():
    try:
        if platform.system().lower() == 'windows':
            networks = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
        elif platform.system().lower() == 'darwin':
            networks = subprocess.check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s'])
        else:
            print("This script is intended for Windows or macOS systems.")
            return

        decoded_nw = networks.decode('ascii')
        print(decoded_nw)
        return decoded_nw

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


decoded_nw = get_wifi_networks()

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1198073744485269566/BNuJdVaqG1WY8KEkBuF9sLQ6OGvMgekDtP-WVpm6Ty_uPDzPqL1MtpFAfI4xBb1OMBKr'
#Personal Discord for testing - kdiaz

data = {
    "content" : "The files have successfully uploaded",
    "username" : "Raspi Upload"
}

result = None

if 'Dunder Mifflin' in decoded_nw:
    print('The network was found!')
    result = requests.post(DISCORD_WEBHOOK_URL, json = data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))
else:
    print('The network was not found.')
