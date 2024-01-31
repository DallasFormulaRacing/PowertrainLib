from mongo_client.mongo_client import Client as MongoClient
import pandas as pd


class Handler:

    @staticmethod
    def mongo_upload_handler():
        mongo_client = MongoClient("dfr_sensor_data", "ecu_data")
        mongo_client.check_connection()


def main():
    handler = Handler()
    handler.mongo_upload_handler()


if __name__ == "__main__":
    main()
