import requests
import jwt
import time
import json
import os
import secrets
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend

TOKEN_URL = "https://api.box.com/oauth2/token"
UPLOAD_URL = "https://upload.box.com/api/2.0/files/content"
USER_INFO_URL = "https://api.box.com/2.0/users/me"

config = json.load(
    open('512311_xk3jq6ao_config.json'))

key_id = config['boxAppSettings']['appAuth']['publicKeyID']


class Client:

    def __init__(self, client_id: str, client_secret: str, file_path: str, folder_id: int):
        self.client_id = config['boxAppSettings']['clientID']
        self.client_secret = config['boxAppSettings']['clientSecret']
        self.file_path = file_path
        self.folder_id = folder_id

    def retrieve_access_token(self) -> str:
        appAuth = config['boxAppSettings']['appAuth']
        private_key = appAuth['privateKey']
        password = appAuth['passphrase']

        key = load_pem_private_key(
            data=private_key.encode('utf8'),
            password=password.encode('utf8'),
            backend=default_backend()
        )

        claims = {
            'iss': config['boxAppSettings']['clientID'],
            'sub': config['enterpriseID'],
            'box_sub_type': 'enterprise',
            'aud': TOKEN_URL,
            'jti': secrets.token_hex(64),
            'exp': int(time.time()) + 60
        }

        assertion = jwt.encode(
            claims,
            key,
            algorithm='RS512',
            headers={
                'kid': key_id
            }
        )

        params = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': assertion,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        try:
            response = requests.post(TOKEN_URL, data=params)

            if response.status_code == 200:

                access_token = response.json().get("access_token")

                return access_token

        except requests.exceptions.RequestException as error:
            print(f'Request Exception: {error}')
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None

    def send_files(self) -> bool:
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

    def get_user_info(self):

        headers = {
            "Authorization": f"Bearer {self.retrieve_access_token()}",
        }

        try:
            response = requests.get(USER_INFO_URL, headers=headers)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code}")
                print(response.json())
                return False
        except requests.exceptions.RequestException as error:
            print(f'Request Exception: {error}')
            return False
