from box_client.box_client import Box_Client
import pytest
import os

@pytest.fixture
def box_client():
    return Box_Client(
        grant_type="client_credentials",
        client_id=os.getenv("CLIENT_ID"),
        client_seceret=os.getenv("CLIENT_SECERET")
    )