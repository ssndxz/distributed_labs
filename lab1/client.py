import socket
import json
import uuid
import time
SERVER_IP = "<SERVERIP>"
PORT = 5000
TIMEOUT = 2      
MAX_RETRIES = 3

request = {
    "request_id": str(uuid.uuid4()),
    "method": "add",
    "params": {
        "a": 5,
        "b": 7
    }
}

attempt = 0
response_received = False

while attempt < MAX_RETRIES and not response_received:
    try:
        print(f"[CLIENT] Attempt {attempt + 1}")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)

        client_socket.connect((SERVER_IP, PORT))
        client_socket.send(json.dumps(request).encode())

        response = client_socket.recv(1024).decode()
        response = json.loads(response)

        print("[CLIENT] Response from server:", response)
        response_received = True

    except socket.timeout:
        print("[CLIENT] Timeout occurred, retrying...")
        attempt += 1
        time.sleep(1)

    except Exception as e:
        print("[CLIENT] Error:", e)
        attempt += 1

    finally:
        client_socket.close()

if not response_received:
    print("[CLIENT] Request failed after retries")
