from pymongo import MongoClient
import time

client = MongoClient()
db = client.skyscanner
collection = db.journey

data = {
    "ori" : "mad",
    "dest": "krk",
    "timestamp": 122222222,
    "month": 8,
    "day": 1,
    "price": 123
}

id_data = collection.insert_one(data).inserted_id

print(int(time.time()))