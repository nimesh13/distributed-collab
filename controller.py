from flask import Flask, json, request
import requests

FILENAME = "hello.txt"
NODE_URL = "http://127.0.0.1:8002"

# Tracking variables for gossip
NEIGHBOURS = []
RECEIVED_MESSAGE_IDS = []

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
        update_id = rqst["id"]
        if update_id in RECEIVED_MESSAGE_IDS:
            return "OK", 200
        else:
            RECEIVED_MESSAGE_IDS.append(update_id)
            with open(FILENAME, "a") as myfile:
                myfile.write(file_update)
            forwardMessage("/file", rqst)
            return "OK", 200
    return {"error": "Request must be JSON"}, 415


# Function for forwarding a message to all neighbours
# Basis of gossip protocol
# Should only be called if the node has not previously received the message before
def forwardMessage(command, json):
    for neighbour in NEIGHBOURS:
        requests.post(neighbour + command, json=json)


# Function for adding neighbours
# Has a check against adding an already existing neighbour
def addNeighbour(IP, port):
    neighbour_string = "http://" + str(IP) + ":" + str(port)
    if neighbour_string not in NEIGHBOURS:
        NEIGHBOURS.append(neighbour_string)