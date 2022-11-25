import uuid
import controller
from controller import app
import argparse
from hlc import HLC
from time import time
from lww import LWW

# Parse initialization parameters
parser = argparse.ArgumentParser()
parser.add_argument('--host', default="0.0.0.0", dest='host', help='Host IP address where this server starts up at.')
parser.add_argument('--port', default="8002", dest='port', help="Port number where this server starts up at.")

args, _ = parser.parse_known_args()
port = args.port
host = args.host
 
if __name__ == "__main__":
    hlc = HLC(int(time()), uuid.uuid4())
    lww = LWW()
    controller.NODE_URL = "http://" + str(host) + ":" + str(port)   # Makes the node URL consistent
    app.config['clock'] = hlc
    app.config['lww'] = lww
    app.run(host=host, port=port)
