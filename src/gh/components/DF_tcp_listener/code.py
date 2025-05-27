#! python3

from ghpythonlib.componentbase import executingcomponent as component
import socket
import threading
import json
import scriptcontext as sc
import Rhino.Geometry as rg
import System.Drawing as sd


class DFTCPListener(component):
    def RunScript(self,
            i_start: bool,
            i_load: bool,
            i_stop: bool,
            i_port: int,
            i_host: str):

        # Sticky defaults
        sc.sticky.setdefault('server_sock', None)
        sc.sticky.setdefault('server_started', False)
        sc.sticky.setdefault('cloud_buffer_raw', [])
        sc.sticky.setdefault('latest_cloud', None)
        sc.sticky.setdefault('status_message', 'Waiting...')
        sc.sticky.setdefault('prev_start', False)
        sc.sticky.setdefault('prev_stop', False)
        sc.sticky.setdefault('prev_load', False)
        sc.sticky.setdefault('client_socks', [])        # Track client sockets

        # Client handler
        def handle_client(conn):
            """
            reads the incoming bytes from a single client socket and stores valid data in a shared buffer
            """
            buf = b''
            with conn:
                while sc.sticky.get('server_started', False):
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
                                sc.sticky['cloud_buffer_raw'] = raw
                    except Exception:
                        break

        # thread to accept incoming connections
        def server_loop(sock):
            """
            runs in its own thread, continuously calling accept() on the listening socket
            Each time a client connects, it launches a new thread running handle_client to deal with that connection
            """
            try:
                conn, _ = sock.accept()
                handle_client(conn)
            except Exception:
                pass

        # Start TCP server
        def start_server():
            """
            creates and binds a TCP socket on the given host/port, marks the server as started and then starts the accept_loop in a background thread
            """
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((i_host, i_port))
            sock.listen(1)
            sc.sticky['server_sock'] = sock
            sc.sticky['server_started'] = True
            sc.sticky['status_message'] = f'Listening on {i_host}:{i_port}'
            # Only accept one connection to keep it long-lived
            threading.Thread(target=server_loop, args=(sock,), daemon=True).start()

        def stop_server():
            sock = sc.sticky.get('server_sock')
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass
            sc.sticky['server_sock'] = None
            sc.sticky['server_started'] = False
            sc.sticky['cloud_buffer_raw'] = []
            sc.sticky['status_message'] = 'Stopped'

        # Start or stop server based on inputs
        if i_start and not sc.sticky['prev_start']:
            start_server()
        if i_stop and not sc.sticky['prev_stop']:
            stop_server()

        # Load buffered points into PointCloud
        if i_load and not sc.sticky['prev_load']:
            raw = sc.sticky.get('cloud_buffer_raw', [])
            if raw:
                pc = rg.PointCloud()
                for x, y, z, r, g, b in raw:
                    pc.Add(rg.Point3d(x, y, z), sd.Color.FromArgb(int(r), int(g), int(b)))
                sc.sticky['latest_cloud'] = pc
                sc.sticky['status_message'] = f'Retrieved {pc.Count} pts'
            else:
                sc.sticky['status_message'] = 'No data buffered'

        # Update previous states
        sc.sticky['prev_start'] = i_start
        sc.sticky['prev_stop'] = i_stop
        sc.sticky['prev_load'] = i_load

        # Update UI and output
        ghenv.Component.Message = sc.sticky['status_message']  # noqa: F821

        o_cloud = sc.sticky['latest_cloud']
        return [o_cloud]
