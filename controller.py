from flask import Flask, json, request, redirect, render_template, url_for
import requests
import os
from time import time
from utils import getUniqueId
from copy import deepcopy

FILENAME = "hello.txt"
NODE_URL = "http://127.0.0.1:8002"

filename = "calendar.json"

# Tracking variables for gossip
NEIGHBOURS = []
RECEIVED_MESSAGE_IDS = []

app = Flask(__name__)
hlc = app.config.get('clock')

@app.route("/", methods=["GET", "POST"])
def home():
    hlc = app.config.get('clock')
    lww = app.config.get('lww')

    # Append event(json object)
    if request.method == "POST":
        event_method = request.form['method']

        if event_method == "POST":
            content = json.dumps(request.form, indent=4)

            hlc.incr(int(time()))
            new_hlc = deepcopy(hlc)
            
            create_event = json.loads(content)
            
            unique_id = getUniqueId(create_event)
            op_success = lww.addSet(unique_id, new_hlc)

            return redirect(url_for('home'))

        elif event_method == "DELETE":
            print("deleted")
            return redirect(url_for('home'))

    # Render User Interface
    return render_template("home.html", data=lww.toJSON())

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

@app.route("/neighbours", methods=["GET"])
def getNeighbours():
    return {"neighbours": NEIGHBOURS}

# Function for forwarding a message to all neighbours
# Basis of gossip protocol
# Should only be called if the node has not previously received the message before
def forwardMessage(command, json):
    for neighbour in NEIGHBOURS:
        requests.post(neighbour + command, json=json)

# Wrapper for adding neighbours
def addNeighbourByIPAndPort(IP, port):
    neighbour_string = "http://" + str(IP) + ":" + str(port)
    addNeighbourFromString(neighbour_string)

# Function for adding neighbours
def addNeighbourFromString(neighbour_string):
    if neighbour_string not in NEIGHBOURS:
        NEIGHBOURS.append(neighbour_string)
    new_neighbours_dict = requests.get(neighbour_string + "/neighbours").json()
    new_neighbours = new_neighbours_dict['neighbours']
    for n in new_neighbours:
        if n not in NEIGHBOURS:
            NEIGHBOURS.append(n)