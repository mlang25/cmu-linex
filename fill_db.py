from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
client.admin.command('ismaster')
db_times = client.restaurants.restaurants

db_times.delete_many({})

for i in range(26):
    db_times.insert_one({'res': {'time': i+2, 'id': i+1}})


