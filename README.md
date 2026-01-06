# Lab 2: Lamport Clocks & Replication
This project implements a distributed key–value store across three EC2 nodes using Lamport clocks for event ordering and Last-Writer-Wins (LWW) for consistency.

## Setup & Run
1. Start Nodes: On each EC2 instance, run the server using its private IP:
- Node A: 
```bash
python3 node.py --id A --port 8000 --peers http://<IP_B>:8001,http://<IP_C>:8002 
```
- Node B:
```bash
python3 node.py --id B --port 8001 --peers http://<IP_A>:8000,http://<IP_C>:8002 
```
- Node C:
```bash
python3 node.py --id C --port 8002 --peers http://<IP_A>:8000,http://<IP_B>:8001 
```
2. Use Client: Use the CLI to interact with the cluster:
```bash
python3 client.py --node http://<IP>:8000 put <key> <value>
```
```bash
python3 client.py --node http://<IP>:8000 get <key>
```
```bash
python3 client.py --node http://<IP>:8000 status
```
