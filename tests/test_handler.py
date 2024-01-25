def test_access_token(box_client):
    request = box_client.retrieve_access_token()
    assert isinstance(request, str)


def test_send_file(box_client):
    request = box_client.send_file()
    assert request == True


def test_get_user_info(box_client):
    request = box_client.get_user_info()
    assert isinstance(request, dict)
