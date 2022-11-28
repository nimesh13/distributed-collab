from random import random
from flask import Flask, json, request, render_template, Response
import requests
from time import time
from utils import getEventId, genUniqueId
from copy import deepcopy
from constants import NEIGHBOURS, MESSAGES, NODE
from hlc import HLC
from message import Message
from lww import LWW

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    hlc = app.config.get('clock')
    lww = app.config.get('lww')

    # Append event(json object)
    if request.method == "POST":
        hlc.incr(int(time()))
        new_hlc = deepcopy(hlc)
        event = json.loads(json.dumps(request.form))
        event_method = request.form['method']

        if event_method == "POST":
            unique_id = getEventId(event)
            lww.addSet(unique_id, new_hlc)
        elif event_method == "DELETE":
            unique_id = getEventId(event)
            lww.removeSet(unique_id, new_hlc)

    # Render User Interface
    return render_template("home.html", data=lww.setToJSONArr())

@app.route("/health")
def healthCheck():
    return "Alive", 200

@app.route("/receive", methods=["POST"])
def receiveMsg():
    request_body = request.json
    msg_id = request_body['msg_id']
    if msg_id not in MESSAGES:
        hlc = app.config.get('clock')
        lww = app.config.get('lww')
        MESSAGES.add(msg_id)
        
        hlc.receive(HLC.unmarshal(request_body['ts']), int(time()))
        msg_lww = LWW.fromJSON(request_body['add'], request_body['remove'])
        lww.merge(msg_lww.add, msg_lww.remove)
        
        gossip('/receive', request_body)
    return 'OK', 200

@app.route("/forward", methods=["POST"])
def forwardMsg():
    hlc = app.config.get('clock')
    lww = app.config.get('lww')

    msg = Message(msgid=genUniqueId(), 
                    add=LWW.toJSON(lww.add),
                    remove=LWW.toJSON(lww.remove),
                    ts=str(hlc)).__dict__
    gossip('/receive', msg)
    return 'OK', 200
    # return Response(msg, mimetype='application/json')

@app.route("/neighbours", methods=["GET"])
def getNeighbours():
    resp = {"neighbours": list(NEIGHBOURS)}
    return Response(json.dumps(resp), mimetype='application/json')

@app.route("/initiate", methods=["POST"])
def initiate():
    request_body = request.json
    if request_body['addr'] not in NEIGHBOURS:
        NEIGHBOURS.add(request_body['addr'])
    
    return 'OK', 200

# Function for forwarding a message to all neighbours
# Basis of gossip protocol
# Should only be called if the node has not previously received the message before
def gossip(uri, body):
    headers = {'Content-type': 'application/json'}
    for neighbour in NEIGHBOURS:
        requests.post(neighbour + uri, json=body, headers=headers)

# Wrapper for adding neighbours
def addNeighbourByIPAndPort(IP, port):
    neighbour_string = "http://" + str(IP) + ":" + str(port)
    addNeighbourFromString(neighbour_string)

# Function for adding neighbours
def addNeighbourFromString(neighbour_string):
    new_neighbours_dict = requests.get(neighbour_string + "/neighbours").json()
    new_neighbours = new_neighbours_dict['neighbours']
    for n in new_neighbours:
        if n not in NEIGHBOURS and n != NODE['URL'] and (len(NEIGHBOURS) < 5 or random() < 0.5):
            NEIGHBOURS.add(n)
            initiateConn(n)

def initiateConn(neighbour, fetch_neighbours=False):
    msg = dict(addr=NODE['URL'])
    headers = {'Content-type': 'application/json'}
    res = requests.post(neighbour + '/initiate', json=msg, headers=headers)
    if res.status_code == 200:
        NEIGHBOURS.add(neighbour)
        if fetch_neighbours:
            addNeighbourFromString(neighbour)