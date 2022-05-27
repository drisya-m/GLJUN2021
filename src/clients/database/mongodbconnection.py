from pymongo import MongoClient


class MongoDBConnection:
    def __init__(self):
        self.connection = None
        self.Database = None

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    def __enter__(self):
        self.connection = MongoClient(
            "mongodb+srv://admin:taxiadmin123@cluster0.2p1ix.mongodb.net/?retryWrites=true&w=majority")
        self.Database = self.connection['taxi_service']
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
