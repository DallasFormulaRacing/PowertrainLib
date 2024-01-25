import requests

class discord_webhook:

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def post_message(self, message: str):
        data = {
            "content": message
        }
        result = requests.post(self.webhook_url, json=data)

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print("Status code: {}".format(result.status_code))