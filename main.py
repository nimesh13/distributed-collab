from flask import Flask, json, request
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(dest='port', help="Port number where this server starts up at.")

# Parse and print the results
args, _ = parser.parse_known_args()
port = args.port

FILENAME = "hello.txt"

app = Flask(__name__)

@app.route("/health")
def healthCheck():
    return "Alive", 200

@app.route("/file", methods=["POST"])
def file():
    if request.is_json:
        rqst = request.get_json()
        file_update = rqst["content"]
        with open(FILENAME, "a") as myfile:
            myfile.write(file_update)
        return "OK", 200
    return {"error": "Request must be JSON"}, 415
    
if __name__ == "__main__":
    app.run(debug=True, port=port)