from pymongo import MongoClient
from bson.json_util import loads, dumps
from datetime import datetime
from config import CONN_STRING


class database:
    def __init__(self):
        client = MongoClient(CONN_STRING)
        client.admin.command("ismaster")
        self.baseline = client.restaurants.baseline
        self.data_points = client.restaurants.data_points
        self.restaurants = client.restaurants.restaurants

    def get_all(self) -> dict:
        add_time_c = self.restaurants.find({}).sort([("res_id", 1)])
        times = {}
        for i in add_time_c:
            times[int(i.get("res_id"))] = i.get("wait_time")
        return times

    def insert_one(self, time_dict):
        self.data_points.insert_one(
            {
                "res_id": time_dict.get("res_id"),
                "wait": time_dict.get("wait_time"),
                "submit_time": datetime.utcnow(),
            }
        )  # insert the datapoint

        calc_waittime = self.__calc_average__(time_dict)
        newWaitTime = {
            "$set": {"wait_time": calc_waittime, "res_id": time_dict.get("res_id")}
        }  # update the restuarant's waittime
        filter = {"res_id": time_dict.get("res_id")}
        self.restaurants.update_one(filter, newWaitTime)
        self.__update_baseline__(calc_waittime, time_dict.get("res_id"))

    def __calc_average__(self, time_dict):
        # get all res_id documents
        c = self.data_points.find({"res_id": time_dict.get("res_id")})
        total_time = 0
        total_weights = 0
        for i in c:
            min_passed = (
                datetime.utcnow() - i.get("submit_time")
            ).total_seconds() // 60  # get submit time of the data point
            total_weights += 15 - min_passed  # weight it linearly
            total_time += i.get("wait") * (15 - min_passed)  # add the average
        return total_time / (total_weights)  # return the weighted average

    def get_future(self, res_id, iso_datetime):
        a = self.baseline.find_one({"res_id": res_id})
        # get the time requested by client
        try:
            time = datetime.fromisoformat(iso_datetime)
        except ValueError:
            return "Invalid ISO format"
        day = time.weekday()  # get the day of the week
        print(day)
        hour = time.hour  # get the hour
        return a.get("days")[day][hour]

    def __update_baseline__(self, newWaitTime, res_id):
        filter = {"res_id": res_id}
        self.baseline.update_one(
            filter,
            {
                "$set": {
                    "days."
                    + str(datetime.now().weekday())
                    + "."
                    + str(datetime.now().hour): newWaitTime
                }
            },
        )

