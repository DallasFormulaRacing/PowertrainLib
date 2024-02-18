from box_client.box_client import Client as Box_Client
from mongo_client.mongo_client import Client as Mongo_Client
import pytest
import os
import json

uri = f"mongodb+srv://noel:${os.getenv('MONGO_PASSWORD')}@cluster0.gw7z3sn.mongodb.net/?retryWrites=true&w=majority"

config = json.load(
    open('512311_xk3jq6ao_config.json')
    )


@pytest.fixture
def box_client():
    return Box_Client(
        client_id=config['boxAppSettings']['clientID'],
        client_secret=config['boxAppSettings']['clientSecret'],
        enterprise_id=config['enterpriseID'],
        key_id=config['boxAppSettings']['appAuth']['publicKeyID'],
        private_key=config['boxAppSettings']['appAuth']['privateKey'],
        password=config['boxAppSettings']['appAuth']['passphrase'],
        file_path=config['file_path'],
        folder_id=config['folder_id']
    )


@pytest.fixture
def mongo_client():
    return Mongo_Client(
        db_name="cluster0",
        collection_name="dfr_sensor_data"
    )
