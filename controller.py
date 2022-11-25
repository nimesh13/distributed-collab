from flask import Flask, json, request, render_template
import requests
from time import time
from utils import getUniqueId
from copy import deepcopy

NODE_URL = "http://127.0.0.1:8002"

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
        hlc.incr(int(time()))
        new_hlc = deepcopy(hlc)
        event = json.loads(json.dumps(request.form))
        
        if event_method == "POST":
            unique_id = getUniqueId(event)
            op_success = lww.addSet(unique_id, new_hlc)
        elif event_method == "DELETE":
            unique_id = getUniqueId(event)
            op_success = lww.removeSet(unique_id, new_hlc)

    # Render User Interface
    return render_template("home.html", data=lww.toJSON())

@app.route("/health")
def healthCheck():
    return "Alive", 200

@app.route("/query")
def queryNode():
    return requests.get(NODE_URL + "/health").content

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