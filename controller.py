from flask import Flask, json, request
import requests

FILENAME = "hello.txt"
NODE_URL = "http://127.0.0.1:8002"

app = Flask(__name__)

@app.route("/health")
def healthCheck():
    return "Alive", 200

@app.route("/query")
def queryNode():
    return requests.get(NODE_URL + "/health").content

@app.route("/file", methods=["POST"])
def file():
    if request.is_json:
        rqst = request.get_json()
        file_update = rqst["content"]
        with open(FILENAME, "a") as myfile:
            myfile.write(file_update)
        return "OK", 200
    return {"error": "Request must be JSON"}, 415