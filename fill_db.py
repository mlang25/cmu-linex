from pymongo import MongoClient
from datetime import datetime
from random import randint

client = MongoClient("mongodb://127.0.0.1:27017")
client.admin.command('ismaster')


def fill_data_points():
    client.restaurants.data_points.drop()
    data_points = client.restaurants.create_collection("data_points", timeseries={
                                                       "timeField": "submit_time", "granularity": "seconds"}, expireAfterSeconds=900)
    for i in range(4):
        data_points.insert_one({'res_id': 1, "wait": randint(
            5, 10), "submit_time": datetime.utcnow()})


def fill_restaurants():
    rest = client.restaurants.restaurants
    rest.delete_many({})
    for i in range(27):
        rest.insert_one({'res_id': i, "wait_time": 0})


def fill_baseline():
    base = client.restaurants.baseline
    base.delete_many({})
    for i in range(27):
        base.insert_one({"res_id": i, "baseline": 5})


fill_restaurants()
fill_baseline()
fill_data_points()
