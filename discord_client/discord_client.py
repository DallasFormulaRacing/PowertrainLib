import traceback

import requests
import logging

logging.basicConfig(level=logging.INFO)


class Client:

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def post_message(self, message: str) -> bool:
        data = {
            "content": message
        }

        try:

            logging.info("Posting message to Discord")
            result = requests.post(self.webhook_url, json=data)
            result.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logging.exception("An error occurred: {}".format(err))
            traceback.print_exc(err)
        else:
            print("Status code: {}".format(result.status_code))
