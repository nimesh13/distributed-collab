# distributed-collab
Simulation of a distributed collaboration tool using a P2P communication network.

CS249 Distributed Systems project - Collaborative Calendar

Team Members:
1. Nimesh Doolani
2. Ivan Hernandez
3. Kevin Prakash

You will need these things installed before you can use this application:
1. python3 or python
2. pip
3. Docker

Follow these steps to use this application locally:

The default host is 0.0.0.0 or localhost - you don't have to mention it in the command line.
You should try both to see which works.

1. `pip install -r requirements.txt`
2. Start the first node in the network as:
    `python3 main.py`
   This will start the node at default address:  http://0.0.0.0:8000
3. Start the second node in the network at any other node, say 8001:
    `python3 main.py --port=8001 --connect_port=8000`
   This will start the node at address: http://0.0.0.0:8001 and
   try to connect to the first node running at port 8000 to initiate a connection.
   After the connection is established, the nodes will be added to each other's
   neighbours list
4. Start consequent nodes using the same command after specifying the port 
   where it should start up and the node it should connect to.
    `python3 main.py --port=8002 --connect_port=8001`

Follow these steps to use this application as a docker container:

The default host is 0.0.0.0 - you don't have to mention it in the command line.

1. Start the first node in the network as:
    `docker build -t colab:1 -f 1.Dockerfile .`
   The dockerfile for this node is 1.Dockerfile and you can update the port it should run on.
   The port mentioned in the file is 8000
   Run the container as:
    `docker run -d -p 8000:8000 colab:1`
   This will run the container and map the ports 8000 of the container with 8000 of the host machine.
2. To start the second node:
   a. The dockerfile for this is 2.Dockerfile
   b. Specify the port where it should run:         --port, 
      port of the node it should connect to:        --connect_port,
      and IP address of the first node container    --connect_host
   c. Build the image as:
        `docker build -t colab:2 -f 2.Dockerfile .`
      Run the container as:
        `docker run -d -p 8001:8001 colab:2`
    This will start up the second node and initiate connection with the first node.
3. Any consequent nodes can be run similarly, with `3.Dockerfile`

To use this application on different devices:
1. The steps are similar as for Docker
2. Start up the first node locally as:
   `python3 main.py`
3. For consequent nodes, the command is:
   `python3 main.py --port=<<insert>> --connect_port=<<insert>> --connect_host=<<insert>>`
   The  `connect_port` and `connect_host` will be the IP and port of the machine where
   the first node is running.
4. You would also need to open ports for the network traffic.

To use the application:
1. Open http://0.0.0.0:8000/ in the browser
2. Open http://0.0.0.0:8001/ in the browser
3. Create/delete events 
4. Send messages using the Forward button. 