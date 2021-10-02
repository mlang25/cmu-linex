from pymongo import MongoClient
from bson.json_util import loads, dumps

class database():
    def __init__(self):
        client = MongoClient("mongodb://127.0.0.1:27017")
        client.admin.command('ismaster')
        self.db_times = client.restaurants.restaurants

    def get_all(self) -> dict:
        cursor = self.db_times.find({})
        times ={}
        for i in cursor:
            times[i.get("res").get("id")] = i.get("res").get("time")
        return times
    
    def get_one(self, rest_id) -> int:
        return self.db_times.find_one({"res.id":rest_id}).get("res").get("time")