from flask import Flask, request, json, Response
from pymongo import MongoClient

class MongoAPI:
    def __init__(self, data):
        self.client = MongoClient("mongodb://localhost:27017/")

        database = data["database"]
        collection = data["collection"]
        cursor = self.client[database]
        self.collection = cursor[collection]

        self.data = data

    def read(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, data):
        print("Writing Data")
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted', 
                            'Document_ID': str(response.inserted_id)}

        return output

    def update(self, data):
        filt = data['Document']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output


if __name__ == "__main__":
    data = {
        "database": "NipunDb",
        "collection": "people",
    }

    mongo_obj = MongoAPI(data)
    print(json.dumps(mongo_obj.read(), indent=4))