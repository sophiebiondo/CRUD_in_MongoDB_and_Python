from pymongo import MongoClient
from pymongo.errors import PyMongoError

class AnimalShelter:
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, user, password, host='localhost', port=8060, db='aac', col='animals'):
        try:
            self.client = MongoClient(
                host=host,
                port=port,
                username=user,
                password=password,
                authSource=db
            )
            self.database = self.client[db]
            self.collection = self.database[col]
        except PyMongoError as e:
            print(f"Connection error: {e}")
            self.client = None

    # CREATE
    def create(self, data):
        if data and isinstance(data, dict):
            try:
                self.collection.insert_one(data)
                return True
            except PyMongoError as e:
                print(f"Insert error: {e}")
        return False

    # READ
    def read(self, query):
        if query and isinstance(query, dict):
            try:
                return list(self.collection.find(query))
            except PyMongoError as e:
                print(f"Read error: {e}")
        return []

    # UPDATE
    def update(self, query, new_values, many=False):
        if query and isinstance(query, dict) and new_values and isinstance(new_values, dict):
            try:
                if many:
                    result = self.collection.update_many(query, {"$set": new_values})
                else:
                    result = self.collection.update_one(query, {"$set": new_values})
                return result.modified_count
            except PyMongoError as e:
                print(f"Update error: {e}")
        return 0

    # DELETE
    def delete(self, query, many=False):
        if query and isinstance(query, dict):
            try:
                if many:
                    result = self.collection.delete_many(query)
                else:
                    result = self.collection.delete_one(query)
                return result.deleted_count
            except PyMongoError as e:
                print(f"Delete error: {e}")
        return 0