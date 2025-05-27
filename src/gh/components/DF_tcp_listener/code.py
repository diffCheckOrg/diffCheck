from ghpythonlib.componentbase import executingcomponent as component
import socket
import threading
import json
import scriptcontext as sc
import Rhino.Geometry as rg
import System.Drawing as sd


class DFHTTPListener(component):
    def RunScript(self, i_load: bool, i_reset: bool, i_port: int, i_host: str):

        # Sticky defaults
        sc.sticky.setdefault('listen_addr', None)
        sc.sticky.setdefault('server_sock', None)
        sc.sticky.setdefault('server_started', False)
        sc.sticky.setdefault('cloud_buffer_raw', [])
        sc.sticky.setdefault('latest_cloud', None)
        sc.sticky.setdefault('status_message', "Waiting...")
        sc.sticky.setdefault('prev_load', False)

        # Handle Reset or host/port change
        addr = (i_host, i_port)
        if i_reset or sc.sticky['listen_addr'] != addr:
            # close old socket if any
            old = sc.sticky.get('server_sock')
            try:
                if old:
                    old.close()
            except Exception:
                pass

            sc.sticky['listen_addr'] = addr
            sc.sticky['server_sock'] = None
            sc.sticky['server_started'] = False
            sc.sticky['cloud_buffer_raw'] = []
            sc.sticky['latest_cloud'] = None
            sc.sticky['status_message'] = "Reset" if i_reset else f"Addr → {i_host}:{i_port}"
        ghenv.Component.Message = sc.sticky['status_message']  # noqa: F821

        # Client handler
        def handle_client(conn):
            buf = b''
            with conn:
                while True:
                    try:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        buf += chunk
                        while b'\n' in buf:
                            line, buf = buf.split(b'\n', 1)
                            try:
                                raw = json.loads(line.decode())
                            except Exception as e:
                                sc.sticky['status_message'] = f"JSON error: {e}"
                                ghenv.Component.Message = sc.sticky['status_message']  # noqa: F821
                                continue

                            if isinstance(raw, list) and all(isinstance(pt, list) and len(pt)==6 for pt in raw):
                                sc.sticky['cloud_buffer_raw'] = raw
                                sc.sticky['status_message'] = f"Buffered {len(raw)} pts"
                            else:
                                sc.sticky['status_message'] = "Unexpected format"
                            ghenv.Component.Message = sc.sticky['status_message']  # noqa: F821
                    except Exception as e:
                        sc.sticky['status_message'] = f"Socket error: {e}"
                        ghenv.Component.Message = sc.sticky['status_message']  # noqa: F821
                        break

        def accept_loop(srv_sock):
            while True:
                try:
                    conn, _ = srv_sock.accept()
                    threading.Thread(target=handle_client, args=(conn,), daemon=True).start()
                except Exception:
                    break

        # Start server
        def start_server():
            try:
                srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                srv.bind((i_host, i_port))
                srv.listen()
                sc.sticky['server_sock'] = srv
                sc.sticky['server_started'] = True
                sc.sticky['status_message'] = f"Listening on {i_host}:{i_port}"
                ghenv.Component.Message = sc.sticky['status_message']  # noqa: F821
                threading.Thread(target=accept_loop, args=(srv,), daemon=True).start()
            except Exception as e:
                sc.sticky['status_message'] = f"Server error: {e}"
                ghenv.Component.Message = sc.sticky['status_message']  # noqa: F821

        if not sc.sticky['server_started']:
            start_server()

        if i_load and not sc.sticky['prev_load']:
            raw = sc.sticky['cloud_buffer_raw']
            if raw:
                pc = rg.PointCloud()
                for x, y, z, r, g, b in raw:
                    col = sd.Color.FromArgb(int(r), int(g), int(b))
                    pc.Add(rg.Point3d(x, y, z), col)
                sc.sticky['latest_cloud']   = pc
                sc.sticky['status_message'] = f"Retrieved {pc.Count} pts"
            else:
                sc.sticky['status_message'] = "No data buffered"
            ghenv.Component.Message = sc.sticky['status_message']  # noqa: F821
        sc.sticky['prev_load'] = i_load

        return [sc.sticky['latest_cloud']]
