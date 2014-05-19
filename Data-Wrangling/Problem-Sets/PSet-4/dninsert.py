import json

def insert_data(data, db):
    # insert data in MongoDB into a collection called 'arachnid'
    for entry in data:
        db.arachnid.insert(entry)


if __name__ == "__main__":
    
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    with open('arachnid.json') as f:
        data = json.loads(f.read())
        insert_data(data, db)
        print db.arachnid.find_one()
