#! python3

from ghpythonlib.componentbase import executingcomponent as component
import threading
import asyncio
import json
import scriptcontext as sc
import Rhino.Geometry as rg
import System.Drawing as sd
from websockets.server import serve
from diffCheck import df_gh_canvas


class DFWSServerListener(component):
    def __init__(self):
        try:
            ghenv.Component.ExpireSolution(True)  # noqa: F821
            ghenv.Component.Attributes.PerformLayout()  # noqa: F821
        except NameError:
            pass

        for idx, label in enumerate(("Start", "Stop", "Load")):
            df_gh_canvas.add_button(
                ghenv.Component, label, idx, x_offset=60)  # noqa: F821
        df_gh_canvas.add_panel(ghenv.Component, "Host", "127.0.0.1", 3, 60, 20)  # noqa: F821
        df_gh_canvas.add_panel(ghenv.Component, "Port", "9000", 4, 60, 20)  # noqa: F821

    def RunScript(self,
            i_start: bool,
            i_stop: bool,
            i_load: bool,
            i_host: str,
            i_port: int):

        prefix = 'ws'

        # Persistent state across runs
        sc.sticky.setdefault(f'{prefix}_ws_server', None)
        sc.sticky.setdefault(f'{prefix}_ws_loop',   None)
        sc.sticky.setdefault(f'{prefix}_ws_thread', None)
        sc.sticky.setdefault(f'{prefix}_last_pcd',  None)
        sc.sticky.setdefault(f'{prefix}_loaded_pcd', None)
        sc.sticky.setdefault(f'{prefix}_ws_logs',   [])
        sc.sticky.setdefault(f'{prefix}_ws_thread_started', False)
        sc.sticky.setdefault(f'{prefix}_prev_start', False)
        sc.sticky.setdefault(f'{prefix}_prev_stop',  False)
        sc.sticky.setdefault(f'{prefix}_prev_load',  False)

        logs = sc.sticky[f'{prefix}_ws_logs']

        # STOP server
        if i_stop and sc.sticky.pop(f'{prefix}_ws_thread_started', False):
            server = sc.sticky.pop(f'{prefix}_ws_server', None)
            loop = sc.sticky.pop(f'{prefix}_ws_loop',   None)
            if server and loop:
                try:
                    server.close()
                    asyncio.run_coroutine_threadsafe(server.wait_closed(), loop)
                    logs.append("WebSocket server close initiated")
                except Exception as e:
                    logs.append(f"Error closing server: {e}")
            sc.sticky[f'{prefix}_ws_thread'] = None
            logs.append("Cleared previous WebSocket server flag")
            ghenv.Component.ExpireSolution(True)  # noqa: F821

        # START server
        if i_start and not sc.sticky[f'{prefix}_ws_thread_started']:

            async def echo(ws, path):
                logs.append("[GH] Client connected")
                try:
                    async for msg in ws:
                        try:
                            pcd = json.loads(msg)
                            if isinstance(pcd, list) and all(isinstance(pt, (list, tuple)) and len(pt) == 6 for pt in pcd):
                                sc.sticky[f'{prefix}_last_pcd'] = pcd
                                logs.append(f"Received PCD with {len(pcd)} points")
                            else:
                                logs.append("Invalid PCD format")
                        except Exception as inner:
                            logs.append(f"PCD parse error: {inner}")
                except Exception as outer:
                    logs.append(f"Handler crashed: {outer}")

            async def server_coro():
                loop = asyncio.get_running_loop()
                sc.sticky[f'{prefix}_ws_loop'] = loop

                logs.append(f"server_coro starting on {i_host}:{i_port}")
                server = await serve(echo, i_host, i_port)
                sc.sticky[f'{prefix}_ws_server'] = server
                logs.append(f"Listening on ws://{i_host}:{i_port}")
                await server.wait_closed()
                logs.append("Server coroutine exited")

            def run_server():
                try:
                    asyncio.run(server_coro())
                except Exception as ex:
                    logs.append(f"WebSocket server ERROR: {ex}")

            t = threading.Thread(target=run_server, daemon=True)
            t.start()
            sc.sticky[f'{prefix}_ws_thread'] = t
            sc.sticky[f'{prefix}_ws_thread_started'] = True
            ghenv.Component.ExpireSolution(True)  # noqa: F821

        # LOAD buffered PCD on i_load rising edge
        if i_load and not sc.sticky[f'{prefix}_prev_load']:
            sc.sticky[f'{prefix}_loaded_pcd'] = sc.sticky.get(f'{prefix}_last_pcd')
            cnt = len(sc.sticky[f'{prefix}_loaded_pcd']) if sc.sticky[f'{prefix}_loaded_pcd'] else 0
            logs.append(f"Loaded pcd with {cnt} pts")
            ghenv.Component.ExpireSolution(True)  # noqa: F821

        # BUILD output PointCloud
        raw = sc.sticky.get(f'{prefix}_loaded_pcd')
        if isinstance(raw, list) and all(isinstance(pt, (list, tuple)) and len(pt) == 6 for pt in raw):
            pc = rg.PointCloud()
            for x, y, z, r, g, b in raw:
                pt = rg.Point3d(x, y, z)
                col = sd.Color.FromArgb(r, g, b)
                pc.Add(pt, col)
            o_cloud = pc
        else:
            o_cloud = None

        # UPDATE UI message & return outputs
        ghenv.Component.Message = logs[-1] if logs else 'Waiting..'  # noqa: F821
        sc.sticky[f'{prefix}_prev_start'] = i_start
        sc.sticky[f'{prefix}_prev_stop']  = i_stop
        sc.sticky[f'{prefix}_prev_load']  = i_load

        return [o_cloud]
