def test_access_token(box_client):
    request = box_client.retrieve_access_token()
    assert isinstance(request, str)


def test_send_files(box_client):
    request = box_client.send_files()
    assert request is True


def test_get_user_info(box_client):
    request = box_client.get_user_info()
    assert isinstance(request, dict)


def test_mongo_connection(mongo_client):
    request = mongo_client.establish_connection()
    assert request is None


def test_mongo_pull(mongo_client):
    request = mongo_client.pull_documents({})
    assert isinstance(request, list)
