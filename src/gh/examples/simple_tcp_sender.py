import socket
import time
import random
import json

host = '127.0.0.1'
port = 5000


def random_colored_point():
    x, y, z = [round(random.uniform(-10, 10), 2) for _ in range(3)]
    r, g, b = [random.randint(0, 255) for _ in range(3)]
    return [x, y, z, r, g, b]


with socket.create_connection((host, port)) as s:
    print("Connected to GH")
    while True:
        cloud = [random_colored_point() for _ in range(1000)]
        msg = json.dumps(cloud) + "\n"
        s.sendall(msg.encode())
        print("Sent cloud with", len(cloud), "colored points")
        time.sleep(1)
