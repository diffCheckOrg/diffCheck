#! python3

from ghpythonlib.componentbase import executingcomponent as component
# import threading
# import asyncio
# import json
import scriptcontext as sc
# import Rhino.Geometry as rg
# import System.Drawing as sd
#import websockets


class DFWSServerListener(component):
    def RunScript(self,
            i_start: bool,
            i_load: bool,
            i_stop: bool,
            i_host: str,
            i_port: int):     # Port to bind

        # --- Persistent state across runs ---
        sc.sticky.setdefault('ws_thread', None)
        sc.sticky.setdefault('ws_loop', None)
        sc.sticky.setdefault('ws_server', None)
        sc.sticky.setdefault('ws_buffer', [])
        sc.sticky.setdefault('ws_latest', None)
        sc.sticky.setdefault('status', 'Idle')
        sc.sticky.setdefault('prev_start', False)
        sc.sticky.setdefault('prev_stop', False)
        sc.sticky.setdefault('prev_load', False)

        # async def handler(ws, path):
        #     """Receive JSON-encoded dicts and buffer valid points."""
        #     try:
        #         async for msg in ws:
        #             data = json.loads(msg)
        #             if isinstance(data, dict) and {'x','y','z'}.issubset(data):
        #                 sc.sticky['ws_buffer'].append(data)
        #                 sc.sticky['status'] = f"Buffered {len(sc.sticky['ws_buffer'])} pts"
        #                 ghenv.Component.ExpireSolution(True)  # noqa: F821
        #     except Exception:
        #         pass

        # def server_thread():
        #     # Create and set a new event loop in this thread
        #     loop = asyncio.new_event_loop()
        #     sc.sticky['ws_loop'] = loop
        #     asyncio.set_event_loop(loop)
        #     try:
        #         # Start the WebSocket server on this loop
        #         start_srv = websockets.serve(handler, i_host, i_port)
        #         server = loop.run_until_complete(start_srv)
        #         sc.sticky['ws_server'] = server
        #         sc.sticky['status'] = f"Listening ws://{i_host}:{i_port}"
        #         ghenv.Component.ExpireSolution(True)  # noqa: F821
        #         # Serve forever until stopped
        #         loop.run_forever()
        #     except Exception as ex:
        #         sc.sticky['status'] = f"Server error: {type(ex).__name__}: {ex}"
        #         ghenv.Component.ExpireSolution(True)  # noqa: F821
        #     finally:
        #         # Cleanup: wait for server to close then shutdown loop
        #         srv = sc.sticky.get('ws_server')
        #         if srv:
        #             loop.run_until_complete(srv.wait_closed())
        #         loop.close()
        #         sc.sticky['ws_loop'] = None
        #         sc.sticky['ws_server'] = None

        # def start():
        #     # Begin server thread on rising edge
        #     if sc.sticky['ws_thread'] is None:
        #         sc.sticky['status'] = 'Starting WebSocket server...'
        #         ghenv.Component.Message = sc.sticky['status']  # noqa: F821
        #         t = threading.Thread(target=server_thread, daemon=True)
        #         sc.sticky['ws_thread'] = t
        #         t.start()

        # def stop():
        #     # Signal server and loop to stop
        #     server = sc.sticky.get('ws_server')
        #     loop   = sc.sticky.get('ws_loop')
        #     if server and loop:
        #         loop.call_soon_threadsafe(server.close)
        #         loop.call_soon_threadsafe(loop.stop)
        #     sc.sticky['status'] = 'Stopped'
        #     sc.sticky['ws_buffer'] = []
        #     sc.sticky['ws_thread'] = None
        #     ghenv.Component.Message = sc.sticky['status']  # noqa: F821

        # # Handle toggles
        # if i_start and not sc.sticky['prev_start']:
        #     start()
        # if i_stop and not sc.sticky['prev_stop']:
        #     stop()
        # if i_load and not sc.sticky['prev_load']:
        #     buf = sc.sticky['ws_buffer']
        #     if buf:
        #         pc = rg.PointCloud()
        #         for pt in buf:
        #             pc.Add(rg.Point3d(pt['x'], pt['y'], pt['z']), sd.Color.White)
        #         sc.sticky['ws_latest'] = pc
        #         sc.sticky['status'] = f"Retrieved {pc.Count} pts"
        #         sc.sticky['ws_buffer'] = []
        #     else:
        #         sc.sticky['status'] = 'No data buffered'
        #     ghenv.Component.Message = sc.sticky['status']  # noqa: F821

        # # Update previous states
        # sc.sticky['prev_start'] = i_start
        # sc.sticky['prev_stop']  = i_stop
        # sc.sticky['prev_load']  = i_load

        # # Always update message
        # ghenv.Component.Message = sc.sticky['status']  # noqa: F821

        # o_cloud = sc.sticky.get('ws_latest')
        # return [o_cloud]
