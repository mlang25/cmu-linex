from flask import Flask, make_response, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "hello"


@app.route("/send", methods = ['GET'])
def get_restaurant_info():
    if request.method != 'GET':
        return make_response('Malformed request', 400)

    json_response = {
        0: 1
    }
    return json_response


@app.route("/submit", methods = ['POST'])
def post_info():
    if request.method != 'POST':
        return make_response('Malformed request', 400)

    return make_response(
        "works",
        200
    )
    

@app.errorhandler(404)
def not_found():
    return make_response("Not found", 404)

app.run()