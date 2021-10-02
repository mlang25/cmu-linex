from flask import Flask, make_response, request, jsonify

import json

from db import database

app = Flask(__name__)


@app.route("/")
def home():
    return "hello"


@app.route("/send", methods=["GET"])
def get_restaurant_info():
    if request.method != "GET":
        return make_response("Malformed request", 400)

    json_response = db.get_all()
    return json_response


@app.route("/submit", methods=["POST"])
def post_info():
    if request.method != "POST":
        return make_response("Malformed request", 400)

    data = request.json
    db.insert_one(data)
    return make_response("works", 200)

@app.route("/get-future", methods=["POST"])
def get_future():
    json_request = request.json
    wait_time = db.get_future(json_request["res_id"],json_request["iso_datetime"])
    if wait_time  == -1:
        return make_response("Invalid ISO format", 400)
    return make_response(str(wait_time),200)



@app.errorhandler(404)
def not_found():
    return make_response("Not found", 404)


db = database()
app.run(host="0.0.0.0", port=5000)
