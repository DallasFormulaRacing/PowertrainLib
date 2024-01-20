from box_client.box_client import Box_Client
import pytest
import os


@pytest.fixture
def box_client():
    return Box_Client(
        grant_type="client_credentials",
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        file_path="/Users/noeljohnson/Documents/GitHub/PowertrainLib/tests/emptyfile.txt",
        folder_id="144833862514"
    )
