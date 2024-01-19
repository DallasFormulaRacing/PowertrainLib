import requests
import json

TOKEN_URL = "https://api.box.com/oauth2/token"

class Box_Client:

    def __init__(self, grant_type: str, client_id: str, client_seceret:str):
        self.grant_type = grant_type
        self.client_id = client_id
        self.client_seceret = client_seceret

    def retrieve_access_token(self) -> str:

        body = {
            'grant_type': self.grant_type,
            'client_id': self.client_id,
            'client_secret': self.client_seceret
        }

        try:
            response = requests.post(TOKEN_URL, data=body)

            access_token = response.json().get("access_token")
            print(f"Token Recieved: {access_token}")
            return access_token
        
        except requests.exceptions.RequestException as error:
            return {'status': 'failure', 'error': str(error)}
        

