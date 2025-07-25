#! python3

from ghpythonlib.componentbase import executingcomponent as component
import socket
import threading
import json
import time
import scriptcontext as sc
import Rhino.Geometry as rg
import System.Drawing as sd
from diffCheck import df_gh_canvas_utils
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

class DFTCPListener(component):
    def __init__(self):
        try:
            ghenv.Component.ExpireSolution(True)  # noqa: F821
            ghenv.Component.Attributes.PerformLayout()  # noqa: F821
        except NameError:
            pass

        for idx, label in enumerate(("Start", "Stop", "Load")):
            df_gh_canvas_utils.add_button(
                ghenv.Component, label, idx, x_offset=60)  # noqa: F821
        df_gh_canvas_utils.add_panel(ghenv.Component, "Host", "127.0.0.1", 3, 60, 20)  # noqa: F821
        df_gh_canvas_utils.add_panel(ghenv.Component, "Port", "5000", 4, 60, 20)  # noqa: F821

    def RunScript(self,
            i_start: bool,
            i_stop: bool,
            i_load: bool,
            i_host: str,
            i_port: int):

        prefix = 'tcp'

        # Sticky initialization
        sc.sticky.setdefault(f'{prefix}_server_sock', None)
        sc.sticky.setdefault(f'{prefix}_server_started', False)
        sc.sticky.setdefault(f'{prefix}_cloud_buffer_raw', [])
        sc.sticky.setdefault(f'{prefix}_latest_cloud', None)
        sc.sticky.setdefault(f'{prefix}_status_message', 'Waiting..')
        sc.sticky.setdefault(f'{prefix}_prev_start', False)
        sc.sticky.setdefault(f'{prefix}_prev_stop', False)
        sc.sticky.setdefault(f'{prefix}_prev_load', False)

        # Client handler
        def handle_client(conn: socket.socket) -> None:
            """
            Reads the incoming bytes from a single TCP client socket and stores valid data in a shared buffer.

            :param conn: A socket object returned by `accept()` representing a live client connection.
                         The client is expected to send newline-delimited JSON-encoded data, where each
                         message is a list of 6D values: [x, y, z, r, g, b].

            :returns: None
            """
            buf = b''
            with conn:
                while sc.sticky.get(f'{prefix}_server_started', False):
                    try:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        buf += chunk
                        while b'\n' in buf:
                            line, buf = buf.split(b'\n', 1)
                            try:
                                raw = json.loads(line.decode())
                            except Exception:
                                continue
                            if isinstance(raw, list) and all(isinstance(pt, list) and len(pt) == 6 for pt in raw):
                                sc.sticky[f'{prefix}_cloud_buffer_raw'] = raw
                    except Exception:
                        break
                    time.sleep(0.05)  # sleep briefly to prevent CPU spin

        # thread to accept incoming connections
        def server_loop(sock: socket.socket) -> None:
            """
            Accepts a single client connection and starts a background thread to handle it.

            :param sock: A bound and listening TCP socket created by start_server().
                         This socket will accept one incoming connection, then delegate it to handle_client().

            :returns: None. This runs as a background thread and blocks on accept().
            """
            try:
                conn, _ = sock.accept()
                handle_client(conn)
            except Exception:
                pass

        # Start TCP server
        def start_server() -> None:
            """
            creates and binds a TCP socket on the given host/port, marks the server as started and then starts the accept_loop in a background thread

            :returns: None.
            """
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((i_host, i_port))
            sock.listen(1)
            sc.sticky[f'{prefix}_server_sock'] = sock
            sc.sticky[f'{prefix}_server_started'] = True
            sc.sticky[f'{prefix}_status_message'] = f'Listening on {i_host}:{i_port}'
            # Only accept one connection to keep it long-lived
            threading.Thread(target=server_loop, args=(sock,), daemon=True).start()

        def stop_server() -> None:
            """
            Stops the running TCP server by closing the listening socket and resetting internal state.

            :returns: None.
            """
            sock = sc.sticky.get(f'{prefix}_server_sock')
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass
            sc.sticky[f'{prefix}_server_sock'] = None
            sc.sticky[f'{prefix}_server_started'] = False
            sc.sticky[f'{prefix}_cloud_buffer_raw'] = []
            sc.sticky[f'{prefix}_status_message'] = 'Stopped'

        # Start or stop server based on inputs
        if i_start and not sc.sticky[f'{prefix}_prev_start']:
            start_server()
        if i_stop and not sc.sticky[f'{prefix}_prev_stop']:
            stop_server()

        # Load buffered points into Rhino PointCloud
        if i_load and not sc.sticky[f'{prefix}_prev_load']:
            if not sc.sticky.get(f'{prefix}_server_started', False):
                self.AddRuntimeMessage(RML.Warning,
                                       "Please start server here before trying to send data from remote device.")
                sc.sticky[f'{prefix}_status_message'] = "Server not started"
            else:
                raw = sc.sticky.get(f'{prefix}_cloud_buffer_raw', [])
                if raw:
                    pc = rg.PointCloud()
                    for x, y, z, r, g, b in raw:
                        pc.Add(rg.Point3d(x, y, z), sd.Color.FromArgb(int(r), int(g), int(b)))
                    sc.sticky[f'{prefix}_latest_cloud'] = pc
                    sc.sticky[f'{prefix}_status_message'] = f'Loaded pcd with {pc.Count} pts'
                else:
                    sc.sticky[f'{prefix}_status_message'] = 'No data buffered'

        # Update previous states
        sc.sticky[f'{prefix}_prev_start'] = i_start
        sc.sticky[f'{prefix}_prev_stop'] = i_stop
        sc.sticky[f'{prefix}_prev_load'] = i_load

        # Update UI and output
        ghenv.Component.Message = sc.sticky[f'{prefix}_status_message']  # noqa: F821

        o_cloud = sc.sticky[f'{prefix}_latest_cloud']
        return [o_cloud]
