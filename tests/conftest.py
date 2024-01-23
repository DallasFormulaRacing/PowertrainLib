from box_client.box_client import Box_Client
import pytest
import os


@pytest.fixture
def box_client():
    return Box_Client(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        file_path="/Users/noeljohnson/Documents/file.txt",
        folder_id="217403389478"
    )
