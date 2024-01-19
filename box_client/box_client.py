import requests
import json

TOKEN_URL = "https://api.box.com/oauth2/token"

class Box_Client:

    def __init__(self, grant_type: str, client_id: str, client_seceret:str):
        self.grant_type = grant_type
        self.client_id = "vey8wix8oegezspv1gn2bs2z296x7yng"
        self.client_seceret = "IwSv2bvp25CGFzaDAqRZv9AZ0jCk5f0g"

    def retrieve_access_token(self) -> str:

        body = {
            'grant_type': self.grant_type,
            'client_id': self.client_id,
            'client_secret': self.client_seceret
        }

        response = requests.post(TOKEN_URL, data=body)

        if response.status_code == 200:
            access_token = response.json().get("access_token")
            print(f"Token Recieved: {access_token}")
            return access_token
        
        print(f"Error:{response.status_code}")
        
        return None

