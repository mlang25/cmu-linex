from pymongo import MongoClient
from datetime import datetime
from random import randint
from config import CONN_STRING

client = MongoClient(CONN_STRING)
client.admin.command("ismaster")


def fill_data_points():
    client.restaurants.data_points.drop()
    data_points = client.restaurants.create_collection(
        "data_points",
        timeseries={"timeField": "submit_time", "granularity": "seconds"},
        expireAfterSeconds=900,
    )
    for i in range(4):
        data_points.insert_one(
            {"res_id": 1, "wait": randint(10, 20), "submit_time": datetime.utcnow()}
        )


def fill_restaurants():
    rest = client.restaurants.restaurants
    rest.delete_many({})
    for i in range(27):
        rest.insert_one({"res_id": i, "wait_time": 10})


def fill_baseline():
    base = client.restaurants.baseline
    base.delete_many({})
    days = []
    for k in range(27):
        days = []
        for i in range(7):
            slots = []
            for j in range(24):
                slots.append(j + 1)
            days.append(slots)
        base.insert_one({"res_id": k, "days": days})


fill_restaurants()
fill_baseline()
fill_data_points()
