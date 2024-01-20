import requests
import json
import os

TOKEN_URL = "https://api.box.com/oauth2/token"
UPLOAD_URL = "https://upload.box.com/api/2.0/files/content"


class Box_Client:

    def __init__(self, grant_type: str, client_id: str, client_secret: str, file_path: str, folder_id: int):
        self.grant_type = grant_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.file_path = file_path
        self.folder_id = folder_id

    def retrieve_access_token(self) -> str:

        body = {
            'grant_type': self.grant_type,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        try:
            response = requests.post(TOKEN_URL, data=body)

            access_token = response.json().get("access_token")
            print(f"Token Recieved: {access_token}")
            return access_token

        except requests.exceptions.RequestException as error:
            return {'status': 'failure', 'error': str(error)}

    def send_file(self) -> bool:
        access_token = self.retrieve_access_token()
        file_name = os.path.basename(self.file_path)

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        with open(self.file_path, 'rb') as file_to_upload:

            files = {
                'file': (file_name, file_to_upload),
                'attributes': (None, json.dumps({'parent': {'id': '217403389478'}})),
            }

            # print(json.dumps({'parent': {'id': '217403389478'}}))

            try:
                response = requests.post(
                    UPLOAD_URL, headers=headers, files=files)

                if response.status_code == 201:
                    return True
                else:
                    print(f"Error: {response.status_code}")
                    print(response.json())
                    return False

            except requests.exceptions.RequestException as error:
                print(f'Request Exception: {error}')
                return False
