import requests
import jwt
import time
import json
import os
import secrets
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
import traceback

TOKEN_URL = os.getenv("TOKEN_URL")
UPLOAD_URL = os.getenv("UPLOAD_URL")
USER_INFO_URL = os.getenv("USER_INFO_URL")


class Client:

    def __init__(self, client_id: str, client_secret: str, enterprise_id: str, key_id: str, private_key: str, password: str, folder_path: str, folder_id: int):
        self.client_id = client_id
        self.client_secret = client_secret
        self.enterprise_id = enterprise_id
        self.key_id = key_id
        self.private_key = private_key
        self.password = password
        self.folder_path = folder_path
        self.folder_id = folder_id

    def retrieve_access_token(self) -> str:
        key_id = self.key_id
        private_key = self.private_key
        password = self.password

        key = load_pem_private_key(
            data=private_key.encode('utf8'),
            password=password.encode('utf8'),
            backend=default_backend()
        )

        claims = {
            'iss': self.client_id,
            'sub': self.enterprise_id,
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

    def send_files(self, filenames: list) -> bool:
        access_token = self.retrieve_access_token()

        for filename in filenames:

            file_name = os.path.basename(filename)

            headers = {
                "Authorization": f"Bearer {access_token}",
            }

            with open(filename, 'rb') as file_to_upload:

                files = {
                    'file': (filename, file_to_upload),
                    'attributes': (None, json.dumps({'parent': {'id': str(self.folder_id)}, 'name': file_name}), 'application/json'),
                }

                try:
                    response = requests.post(UPLOAD_URL, headers=headers, files=files)

                    if response.status_code == 201:
                        continue
                    else:
                        print(f"Error: {response.status_code}")
                        print(response.json())
                        return False

                except requests.exceptions.RequestException as error:
                    print(f'Request Exception: {error}')
                    return False

        return True

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

    def discover_files(self) -> list:

        list_of_files = []

        if os.path.exists(self.folder_path) and os.path.isdir(self.folder_path):
            files = os.listdir(self.folder_path)

            for file in files:
                list_of_files.append("C:\\Users\\sajip\\OneDrive\\Desktop\\" + file)
                print(file)

            return list_of_files

        return None
