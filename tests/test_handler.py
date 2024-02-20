def test_access_token(box_client):
    request = box_client.retrieve_access_token()
    assert isinstance(request, str)


def test_send_files(box_client):

    list_of_files = [
        "C:\\Users\\sajip\\Documents\\GitHub\\PowertrainLib\\files\\ecu4.csv",
        "C:\\Users\\sajip\\Documents\\GitHub\\PowertrainLib\\files\\ecu2.csv"
    ]

    request = box_client.send_files(list_of_files)
    assert request is True


def test_get_user_info(box_client):
    request = box_client.get_user_info()
    assert isinstance(request, dict)


def test_discover_file(box_client):
    file_exist = box_client.discover_files()
    assert file_exist is True


def test_mongo_connection(mongo_client):
    request = mongo_client.establish_connection()
    assert request is None


def test_mongo_pull(mongo_client):
    request = mongo_client.pull_documents({})
    assert isinstance(request, list)
