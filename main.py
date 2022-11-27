from uuid import uuid1
import controller
from controller import app, initiateConn
import argparse
from hlc import HLC
from time import time
from lww import LWW

# Parse initialization parameters
parser = argparse.ArgumentParser()
parser.add_argument('--host', default="0.0.0.0", dest='host', help='Host IP address where this server starts up at.')
parser.add_argument('--port', default="8002", dest='port', help="Port number where this server starts up at.")
parser.add_argument('--connect', dest='connect', help='Address of the node you would like to connect to.')

args, _ = parser.parse_known_args()
port = args.port
host = args.host
connect = args.connect
 
if __name__ == "__main__":
    hlc = HLC(int(time()), str(uuid1()))
    lww = LWW()
    controller.NODE_URL = "http://" + str(host) + ":" + str(port)   # Makes the node URL consistent
    app.config['clock'] = hlc
    app.config['lww'] = lww
    if connect:
        initiateConn(connect)
    app.run(host=host, port=port)
