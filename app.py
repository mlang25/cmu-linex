from flask import Flask, make_response, request, jsonify

app = Flask(__name__)

@app.route("/send", methods = ['GET'])
def get_restaurant_info():
    if request.method != 'GET':
        return make_response('Malformed request', 400)

    return make_response(
        "Success",
        200,
        headers = headers
    )


@app.get("/submit", methods = ['POST'])
def post_info():
    if request.method != 'POST':
        return make_response('Malformed request', 400)
    

@app.errorhandler(404)
def not_found():
    return make_response("Not found" 404)