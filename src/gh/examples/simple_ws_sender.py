# import asyncio
# import websockets
# import json
# import random

URI = "ws://127.0.0.1:8765"  # match i_host and i_port on your GH component
SEND_INTERVAL = 2.0         # seconds between sends


# async def send_points(uri):
#     """
#     Connects once to the WebSocket server and then
#     sends a random point dict every SEND_INTERVAL seconds.
#     """
#     async with websockets.connect(uri) as ws:
#         print(f"Connected to {uri}")
#         while True:
#             # Generate a random point
#             pt = {
#                 "x": random.uniform(0, 10),
#                 "y": random.uniform(0, 10),
#                 "z": random.uniform(0, 10),
#             }
#             msg = json.dumps(pt)
#             await ws.send(msg)
#             print(f"Sent point: {pt}")
#             await asyncio.sleep(SEND_INTERVAL)


# def main():
#     try:
#         asyncio.run(send_points(URI))
#     except KeyboardInterrupt:
#         print("\nSender interrupted and exiting.")

# if __name__ == "__main__":
#     main()
