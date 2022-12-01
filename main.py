from uuid import uuid1
from controller import app, initiateConn
import argparse
from hlc import HLC
from time import time
from lww import LWW
from constants import NODE
import socket 

# Parse initialization parameters
parser = argparse.ArgumentParser()
parser.add_argument('--host', default="0.0.0.0", dest='host', help='Host IP address where this server starts up at.')
parser.add_argument('--port', default="8000", dest='port', help="Port number where this server starts up at.")
parser.add_argument('--connect_port', dest='connect_port', help='Address Port of the node you would like to connect to.')
parser.add_argument('--connect_host', default="0.0.0.0", dest='connect_host', help='Address Host of the node you would like to connect to.')

args, _ = parser.parse_known_args()
NODE['PORT'] = args.port
NODE['HOST'] = args.host
NODE['URL'] = "http://" + socket.gethostbyname(socket.gethostname()) + ":" + NODE['PORT']
CONNECT_PORT = args.connect_port
CONNECT_HOST = args.connect_host

if __name__ == "__main__":
    hlc = HLC(int(time()), str(uuid1()))
    lww = LWW()
    app.config['clock'] = hlc
    app.config['lww'] = lww
    if CONNECT_PORT:
        initiateConn("http://" + CONNECT_HOST + ":" + CONNECT_PORT, fetch_neighbours=True)
    app.run(host=NODE['HOST'], port=NODE['PORT'])
