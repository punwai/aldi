import socket
import json

HOST = "169.254.190.228"
PORT = 65433

# send port message to listening socket
def send_port_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(bytes(json.dumps(message), 'utf-8'))
        data = s.recv(1024)

    print(f"Received {data!r}")

send_port_message({"344343": "33"})