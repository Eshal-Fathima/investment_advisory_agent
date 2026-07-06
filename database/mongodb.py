import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


def connect_db():
    """
    Connect to MongoDB Atlas and return the conversations collection.
    """

    client = MongoClient(os.getenv("MONGODB_URI"))

    database = client[os.getenv("DATABASE_NAME")]

    collection = database[os.getenv("COLLECTION_NAME")]

    return collection