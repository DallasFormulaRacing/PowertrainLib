from box_client.box_client import Client as Box_Client
from mongo_client.mongo_client import Client as Mongo_Client
import pytest
import os

uri = f"mongodb+srv://noel:${os.getenv('MONGO_PASSWORD')}@cluster0.gw7z3sn.mongodb.net/?retryWrites=true&w=majority"


@pytest.fixture
def box_client():
    return Box_Client(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        file_path="/Users/noeljohnson/Documents/file.txt",
        folder_id="217403389478"
    )


@pytest.fixture
def mongo_client():
    return Mongo_Client(
        connection_string=uri
    )
