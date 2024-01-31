from mongo_client.mongo_client import Client as Mongo_Client
import pandas as pd


class Handler:

    @staticmethod
    def mongo_upload_handler():
        mongo_client = Mongo_Client("cluster0", "dfr_sensor_data")
        mongo_client.check_connection()

        ecu_df = pd.read_csv("data/ecu_data/ecu_data.csv")
        ecu_dict = ecu_df.to_dict("records")

        # mongo_client.insert_documents(ecu_dict)
        mongo_client.close_connection()


def main():
    handler = Handler()
    handler.mongo_upload_handler()


if __name__ == "__main__":
    main()
