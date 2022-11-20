from flask import Flask, json, request, redirect, render_template, url_for
import requests
import os

FILENAME = "hello.txt"
NODE_URL = "http://127.0.0.1:8002"

filename = "calendar.json"

# Tracking variables for gossip
NEIGHBOURS = []
RECEIVED_MESSAGE_IDS = []

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    # Create json file if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([], f)

    # Load local json
    json_file = open(filename)
    json_obj = json.load(json_file)

    if request.method == "POST":
        content = json.dumps(request.form, indent=4)
        json_obj.append(json.loads(content))

        # Update local json file
        with open(filename, "w") as f:
            json.dump(json_obj, f, indent=4, separators=(',', ': '))

        return redirect(url_for('home'))

    # Render User Interface
    return render_template("home.html", data=json.dumps(json_obj, indent=4))

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