from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os


class Client:

    client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.clientclient = MongoClient(
            connection_string, server_api=ServerApi('1'))

    def establish_connection(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(f"An error occurred: {e}")

    def close_connection(self):
        self.client.close()
        print("MongoDB connection closed.")

    def insert_document(self, db_name: str, collection_name: str, data: dict):
        try:
            db = self.client[db_name]
            collection = db[collection_name]

            inserted_ids = collection.insert_many(data).inserted_ids
            print(f"Documents inserted, IDs: {inserted_ids}")
        except Exception as e:
            print(f"An error occurred: {e}")
