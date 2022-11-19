from controller import app
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(dest='port', help="Port number where this server starts up at.")

# Parse and print the results
args, _ = parser.parse_known_args()
port = args.port
 
if __name__ == "__main__":
    app.run(debug=True, port=port)