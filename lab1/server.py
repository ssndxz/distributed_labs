import socket
import json
import time
HOST = "0.0.0.0"
PORT = 5000

def add(a, b):
    return a+b
def reverse_string(s):
    return s[::-1]
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"[SERVER] Listening on port {PORT}...")

while True:
    conn, addr = server_socket.accept()
    print(f"[SERVER] Connection from {addr}")

    try:
        data = conn.recv(1024).decode()
        if not data:
            conn.close()
            continue

        request = json.loads(data)
        print(f"[SERVER] Received request: {request}")
        time.sleep(5)

        request_id = request["request_id"]
        method = request["method"]
        params = request["params"]

        if method == "add":
            result = add(params["a"], params["b"])
        elif method == "reverse_string":
            result = reverse_string(params["s"])
        else:
            result = "Unknown method"

        response = {
            "request_id": request_id,
            "result": result,
            "status": "OK"
        }

        conn.send(json.dumps(response).encode())
        print(f"[SERVER] Response sent: {response}")

    except Exception as e:
        print("[SERVER] Error:", e)
    conn.close()
