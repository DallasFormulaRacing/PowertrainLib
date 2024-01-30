import traceback

import requests


class Client:

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    # make this return a boolean
    def post_message(self, message: str) -> bool:
        data = {
            "content": message
        }
        result = requests.post(self.webhook_url, json=data)

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            traceback.print_exc(err)
        else:
            print("Status code: {}".format(result.status_code))
