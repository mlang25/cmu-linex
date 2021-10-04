from pymongo import MongoClient
from datetime import datetime
from random import randint
import json
from config import CONN_STRING

client = MongoClient(CONN_STRING)
client.admin.command("ismaster")


def fill_data_points():
    client.restaurants.data_points.drop()
    data_points = client.restaurants.create_collection(
        "data_points",
        timeseries={"timeField": "submit_time", "granularity": "seconds"},
        expireAfterSeconds=3600,
    )
    for j in range(26):
        for i in range(4):
            data_points.insert_one(
                {"res_id": j, "wait": float(randint(10, 25)), "submit_time": datetime.utcnow()}
            )


def fill_restaurants():
    rest = client.restaurants.restaurants
    rest.delete_many({})
    for i in range(26):
        rest.insert_one({"res_id": i, "wait_time": 10})


def fill_baseline():
    base = client.restaurants.baseline
    base.delete_many({})
    days = []
    for k in range(26):
        days = []
        for i in range(7):
            slots = []
            for j in range(24):
                slots.append(j + 1)
            days.append(slots)
        base.insert_one({"res_id": k, "days": days})


def fill_business_hours():
    business_hours_db = client.restaurants.business_hours
    business_hours_db.delete_many({})
    with open("restaurant-timing.json") as f:
        business_hours = json.load(f)
    for i in range(26):
        operating_hours = []
        for j in range(7):
            daily_hours = []
            open_time = business_hours.get(str(i))[j][0] + 4
            close_time = business_hours.get(str(i))[j][1] + 4
            daily_hours.append(open_time)
            daily_hours.append(close_time)
            operating_hours.append(daily_hours)
        business_hours_db.insert_one({"res_id": i, "times": operating_hours})


'''fill_restaurants()
fill_baseline()'''
fill_data_points()
#fill_business_hours()
