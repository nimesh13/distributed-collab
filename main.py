import controller
from controller import app
import argparse

# Parse initialization parameters
parser = argparse.ArgumentParser()
parser.add_argument('--host', default="127.0.0.1", dest='host', help='Host IP address where this server starts up at.')
parser.add_argument('--port', default="8002", dest='port', help="Port number where this server starts up at.")

args, _ = parser.parse_known_args()
port = args.port
host = args.host

if __name__ == "__main__":
    controller.NODE_URL = "http://" + str(host) + ":" + str(port)  # Makes the node URL consistent
    app.run(debug=True, host=host, port=port)