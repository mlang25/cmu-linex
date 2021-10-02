from pymongo import MongoClient
from bson.json_util import loads, dumps
from datetime import datetime
from config import CONN_STRING


class database():
    def __init__(self):
        client = MongoClient(CONN_STRING)
        client.admin.command('ismaster')
        self.db_times = client.restaurants.restaurants
        self.data_points = client.restaurants.data_points
        self.restaurants = client.restaurants.restaurants

    def get_all(self) -> dict:
        cursor = self.db_times.find({})
        times = {}
        for i in cursor:
            times[int(i.get("res_id"))] = i.get("wait_time")
        return times

    def get_one(self, rest_id) -> int:
        return self.db_times.find_one({"res.id": rest_id}).get("res").get("time")

    def insert_one(self, time_dict):
        self.data_points.insert_one(
            {"res_id": time_dict.get("res_id"), "wait": time_dict.get("res_time"), "submit_time": datetime.utcnow()})

        newWaitTime = {"$set": {"wait_time": self.__calc_average__(
            time_dict), "res_id": time_dict.get("res_id")}}
        filter = {'res_id': time_dict.get("res_id")}
        self.restaurants.update_one(filter, newWaitTime)

    def __calc_average__(self, time_dict):
        c = self.data_points.find({"res_id": time_dict.get("res_id")})
        total_time = 0
        total_weights = 0
        for i in c:
            min_passed = (datetime.utcnow() - i.get("submit_time")
                          ).total_seconds() // 60
            print(min_passed)
            total_weights += 15-min_passed
            total_time += i.get("wait") * (15-min_passed)
        return total_time / (total_weights)
