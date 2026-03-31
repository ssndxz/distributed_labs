# Lab 4: Distributed Transactions (2PC/3PC) Deployment

This project implements a distributed transaction system using Two-Phase Commit (2PC) and Three-Phase Commit (3PC) protocols across 3–5 nodes. It ensures the "All-or-Nothing" atomicity property for operations across multiple resource managers, featuring fault tolerance through Write-Ahead Logging (WAL) and non-blocking coordination in 3PC.

## Setup & Run

1. Start Participants: On each instance, run a participant node. Each node manages its own local storage and Write-Ahead Log.
- Node B: 
```bash
python3 participant.py --id NodeB --port 8001 --wal nodeB.wal
```
```bash
python3 participant.py --id NodeD --port 8002 --wal nodeD.wal
```
```bash
python3 participant.py --id NodeE --port 8003 --wal nodeE.wal
```
2. Start Coordinator: Run the coordinator node, providing the list of all participant URLs:
```bash
python3 coordinator.py --id COORD --port 8000 --participants http://<IP_B>:8001,http://<IP_D>:8002,http://<IP_E>:8003
```
3. Use Client: Trigger a transaction using either the 2PC or 3PC protocol:
```bash
python3 client.py --coord http://<COORD_IP>:8000 start TX123 2PC SET account 500
```
## System Requirements
* Atomic Commitment: Ensures that even if nodes fail, a transaction is either committed on all participants or aborted on all.
* 2PC Implementation: Uses a PREPARE and COMMIT/ABORT cycle. Provides safety but demonstrates the "Blocking Problem" if the coordinator crashes after votes are collected.
* 3PC Implementation: Adds a PreCommit phase and timeout logic to allow participants to reach a decision without the coordinator, avoiding indefinite blocking.
* Write-Ahead Logging (WAL): Every state change (READY, PRECOMMIT, etc.) is persisted to disk. Upon restart, nodes replay the WAL to recover their state and maintain consistency.
* Failure Scenarios: Handles participant timeouts (resulting in Global Abort) and coordinator crashes (resulting in blocking for 2PC or automated resolution for 3PC).
