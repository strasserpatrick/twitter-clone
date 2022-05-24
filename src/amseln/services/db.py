from pprint import pprint

from pymongo import MongoClient

from src.amseln.app import MONGO_DB_PORT, MONGO_DB_URL

# https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb

if __name__ == "__main__":
    client = MongoClient(f"{MONGO_DB_URL}:{MONGO_DB_PORT}")
    db = client.admin
    serverStatusResult = db.command("serverStatus")
    pprint(serverStatusResult)
