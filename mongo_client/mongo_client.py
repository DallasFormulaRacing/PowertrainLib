import traceback
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)


class Client:

    def __init__(self, db_name: str, collection_name: str):
        connection_string = os.getenv("MONGO_URI")
        self.client = MongoClient(connection_string, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        logging.info("MongoDB has been connection established.")

    def check_connection(self) -> bool:

        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            logging.info("MongoDB has been connection established.")
            return True

        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"An error occurred while trying to connect to MongoDB: {e}")
            traceback.print_exc()
            return False

    def close_connection(self) -> bool:

        try:
            self.client.close()
            logging.info("MongoDB connection closed.")
            print("MongoDB connection closed.")
            return True

        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"An error occurred while trying to close the MongoDB connection: {e}")
            traceback.print_exc()
            return False

    def insert_documents(self, data: list) -> bool:

        try:
            if isinstance(data, list):
                inserted_ids = self.collection.insert_many(data).inserted_ids
                logging.info(f"Documents inserted, IDs: {inserted_ids}")
                print(f"Documents inserted, IDs: {inserted_ids}")
                return True

            raise ValueError("Data should be a list of dictionaries")

        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"An error occurred while trying to insert documents: {e}")
            traceback.print_exc()
            return False

    def pull_documents(self, query: dict) -> pd.DataFrame:

        try:
            if isinstance(query, dict):
                documents = list(self.collection.find(query))
                logging.info(f"Documents pulled: {documents}")
                documents_df = pd.DataFrame(documents)

                # print(f"Documents pulled: {documents}")
                documents_df.to_csv('ecu_data_mongo.csv', index=False)

                return documents_df

            raise ValueError("Query should be a dictionary")

        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"An error occurred while trying to pull documents: {e}")
            traceback.print_exc()
            return None
