from uuid import uuid1
from controller import app, initiateConn
import argparse
from hlc import HLC
from time import time
from lww import LWW
from constants import NODE

# Parse initialization parameters
parser = argparse.ArgumentParser()
parser.add_argument('--host', default="0.0.0.0", dest='host', help='Host IP address where this server starts up at.')
parser.add_argument('--port', default="8002", dest='port', help="Port number where this server starts up at.")
parser.add_argument('--connect', dest='connect', help='Address of the node you would like to connect to.')

args, _ = parser.parse_known_args()
NODE['PORT'] = args.port
NODE['HOST'] = args.host
NODE['URL'] = "http://" + NODE['HOST'] + ":" + NODE['PORT']
CONNECT = args.connect

if __name__ == "__main__":
    hlc = HLC(int(time()), str(uuid1()))
    lww = LWW()
    app.config['clock'] = hlc
    app.config['lww'] = lww
    if CONNECT:
        initiateConn(CONNECT)
    app.run(host=NODE['HOST'], port=NODE['PORT'])
