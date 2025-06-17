import asyncio
import websockets
import random
import json


def random_colored_point():
    x, y, z = [round(random.uniform(-10, 10), 2) for _ in range(3)]
    r, g, b = [random.randint(0, 255) for _ in range(3)]
    return [x, y, z, r, g, b]


async def send_pointcloud(host="127.0.0.1", port=8765):
    uri = f"ws://{host}:{port}"
    print(f"Connecting to {uri}…")
    try:
        async with websockets.connect(uri) as ws:
            counter = 0
            while True:
                counter += 1
                # generate and send 1 000 random points
                pcd = [random_colored_point() for _ in range(1000)]
                await ws.send(json.dumps(pcd))
                print(f"[{counter}] Sent PCD with {len(pcd)} points")
                await asyncio.sleep(5)

    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(send_pointcloud(host="127.0.0.1", port=9000))
