from enum import Enum


class Messages(str, Enum):
    MONGO_SUCCESS_MESSAGE = "Docuemnts inserted Successfully"
    MONGO_ERROR_MESSAGE = "An error occurred while trying to connect to MongoDB: {e}"
    MONGO_CLOSE_MESSAGE = "MongoDB connection closed."
    BOX_SUCCESS_MESSAGE = "Files uploaded successfully"
    BOX_ERROR_MESSAGE = "Error occurred while trying to upload files to Box"
    WIFI_SUCCESS_MESSAGE = "Connected to network successfully"
    WIFI_ERROR_MESSAGE = "Error occurred while trying to connect to network"
