from ghpythonlib.componentbase import executingcomponent as component
import socket
import threading
import json
import time
import scriptcontext as sc
import Rhino.Geometry as rg
import System.Drawing as sd
import Grasshopper
from diffCheck import df_gh_canvas_utils

class DFTCPListener(component):
    def __init__(self):
        super(DFTCPListener, self).__init__()
        try:
            ghenv.Component.ExpireSolution(True)  # noqa: F821
            ghenv.Component.Attributes.PerformLayout()  # noqa: F821
        except:
            pass

        for idx, label in enumerate(("Start", "Stop", "Load")):
            df_gh_canvas_utils.add_button(ghenv.Component, label, idx, x_offset=60)  # noqa: F821
        df_gh_canvas_utils.add_panel(ghenv.Component, "Host", "127.0.0.1", 3, 60, 20)  # noqa: F821
        df_gh_canvas_utils.add_panel(ghenv.Component, "Port", "5000", 4, 60, 20)  # noqa: F821

    def RunScript(self, i_start, i_stop, i_load, i_host, i_port):
        prefix = "tcp"

        # ----------------------------
        # Sticky initialization
        # ----------------------------
        sc.sticky.setdefault(prefix + "_server_sock", None)
        sc.sticky.setdefault(prefix + "_server_started", False)
        sc.sticky.setdefault(prefix + "_cloud_buffer_raw", [])
        sc.sticky.setdefault(prefix + "_latest_cloud", None)
        sc.sticky.setdefault(prefix + "_status_message", "Waiting..")
        sc.sticky.setdefault(prefix + "_prev_start", False)
        sc.sticky.setdefault(prefix + "_prev_stop", False)
        sc.sticky.setdefault(prefix + "_prev_load", False)

        # Receiving state
        sc.sticky.setdefault(prefix + "_is_receiving", False)
        sc.sticky.setdefault(prefix + "_recv_bytes", 0)

        # Loading state
        sc.sticky.setdefault(prefix + "_is_loading", False)
        sc.sticky.setdefault(prefix + "_load_progress", (0, 0))  # (done, total)
        sc.sticky.setdefault(prefix + "_load_started_at", None)
        sc.sticky.setdefault(prefix + "_load_duration_s", None)

        # ----------------------------
        # Helper: schedule safe refresh on GH UI/solution thread
        # ----------------------------
        def request_expire(delay_ms=200, recompute=True):
            try:
                comp = ghenv.Component  # noqa: F821
                doc = comp.OnPingDocument()
                if doc is None:
                    return

                def cb(_):
                    try:
                        comp.ExpireSolution(recompute)
                    except:
                        pass

                doc.ScheduleSolution(int(delay_ms), Grasshopper.Kernel.GH_Document.GH_ScheduleDelegate(cb))
            except:
                pass

        # ----------------------------
        # TCP receive thread
        # ----------------------------
        def handle_client(conn):
            buf = b""
            sc.sticky[prefix + "_is_receiving"] = True
            sc.sticky[prefix + "_recv_bytes"] = 0
            sc.sticky[prefix + "_status_message"] = "Client connected; receiving..."
            request_expire(0, True)

            with conn:
                while sc.sticky.get(prefix + "_server_started", False):
                    try:
                        chunk = conn.recv(65536)
                        if not chunk:
                            break
                        sc.sticky[prefix + "_recv_bytes"] += len(chunk)
                        buf += chunk

                        # Expect ONE message terminated by '\n'
                        if b"\n" in buf:
                            line, buf = buf.split(b"\n", 1)

                            try:
                                raw = json.loads(line.decode("utf-8"))
                            except Exception as e:
                                sc.sticky[prefix + "_status_message"] = "JSON error: {}".format(repr(e))
                                request_expire(0, True)
                                break

                            if isinstance(raw, list) and all(isinstance(pt, list) and len(pt) == 6 for pt in raw):
                                sc.sticky[prefix + "_cloud_buffer_raw"] = raw
                                sc.sticky[prefix + "_status_message"] = "Buffered {} pts".format(len(raw))
                            else:
                                sc.sticky[prefix + "_status_message"] = "Invalid payload (expected [[x,y,z,r,g,b],...])"

                            request_expire(0, True)
                            break

                    except Exception as e:
                        sc.sticky[prefix + "_status_message"] = "Recv error: {}".format(repr(e))
                        request_expire(0, True)
                        break

            sc.sticky[prefix + "_is_receiving"] = False
            request_expire(0, True)

        def server_loop(sock):
            try:
                conn, _ = sock.accept()
                handle_client(conn)
            except Exception as e:
                sc.sticky[prefix + "_status_message"] = "Accept error: {}".format(repr(e))
                request_expire(0, True)

        def start_server():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((i_host, int(i_port)))
            sock.listen(1)

            sc.sticky[prefix + "_server_sock"] = sock
            sc.sticky[prefix + "_server_started"] = True
            sc.sticky[prefix + "_status_message"] = "Listening on {}:{}".format(i_host, i_port)

            threading.Thread(target=server_loop, args=(sock,), daemon=True).start()
            request_expire(0, True)

        def stop_server():
            sock = sc.sticky.get(prefix + "_server_sock")
            if sock:
                try:
                    sock.close()
                except:
                    pass

            sc.sticky[prefix + "_server_sock"] = None
            sc.sticky[prefix + "_server_started"] = False
            sc.sticky[prefix + "_is_receiving"] = False
            sc.sticky[prefix + "_is_loading"] = False
            sc.sticky[prefix + "_cloud_buffer_raw"] = []
            sc.sticky[prefix + "_status_message"] = "Stopped"
            request_expire(0, True)

        # ----------------------------
        # Async load (build Rhino PointCloud)
        # ----------------------------
        def build_pointcloud_async(raw_snapshot):
            try:
                sc.sticky[prefix + "_is_loading"] = True
                sc.sticky[prefix + "_load_started_at"] = time.time()
                sc.sticky[prefix + "_load_duration_s"] = None

                total = len(raw_snapshot)
                sc.sticky[prefix + "_load_progress"] = (0, total)
                sc.sticky[prefix + "_status_message"] = "Loading {} pts...".format(total)
                request_expire(0, True)

                pc = rg.PointCloud()

                step = 25000 if total > 25000 else 5000
                last_ui = time.time()

                for i, pt in enumerate(raw_snapshot):
                    x, y, z, r, g, b = pt
                    pc.Add(rg.Point3d(x, y, z), sd.Color.FromArgb(int(r), int(g), int(b)))

                    if (i + 1) % step == 0:
                        sc.sticky[prefix + "_load_progress"] = (i + 1, total)
                        now = time.time()
                        if now - last_ui > 0.3:
                            request_expire(0, True)
                            last_ui = now

                sc.sticky[prefix + "_latest_cloud"] = pc

                dur = time.time() - sc.sticky[prefix + "_load_started_at"]
                sc.sticky[prefix + "_load_duration_s"] = dur
                sc.sticky[prefix + "_load_progress"] = (total, total)
                sc.sticky[prefix + "_status_message"] = "Loaded {} pts in {:.2f}s".format(pc.Count, dur)

                # Force final recompute so output updates immediately
                request_expire(0, True)

            except Exception as e:
                sc.sticky[prefix + "_status_message"] = "Load error: {}".format(repr(e))
                request_expire(0, True)
            finally:
                sc.sticky[prefix + "_is_loading"] = False
                request_expire(0, True)

        # ----------------------------
        # UI: start/stop/load button edges
        # ----------------------------
        if i_start and not sc.sticky[prefix + "_prev_start"]:
            start_server()

        if i_stop and not sc.sticky[prefix + "_prev_stop"]:
            stop_server()

        if i_load and not sc.sticky[prefix + "_prev_load"]:
            if not sc.sticky.get(prefix + "_server_started", False):
                sc.sticky[prefix + "_status_message"] = "Start Server First!"
            elif sc.sticky.get(prefix + "_is_loading", False):
                sc.sticky[prefix + "_status_message"] = "Already loading..."
            else:
                raw = sc.sticky.get(prefix + "_cloud_buffer_raw", [])
                if raw:
                    raw_snapshot = list(raw)  # snapshot
                    threading.Thread(target=build_pointcloud_async, args=(raw_snapshot,), daemon=True).start()
                else:
                    sc.sticky[prefix + "_status_message"] = "No data buffered"
            request_expire(0, True)

        # ----------------------------
        # Live status while receiving/loading
        # ----------------------------
        if sc.sticky.get(prefix + "_is_receiving", False):
            b = sc.sticky.get(prefix + "_recv_bytes", 0)
            sc.sticky[prefix + "_status_message"] = "Receiving... {:.1f} MB".format(b / (1024.0 * 1024.0))
            request_expire(300, True)

        if sc.sticky.get(prefix + "_is_loading", False):
            done, total = sc.sticky.get(prefix + "_load_progress", (0, 0))
            if total:
                sc.sticky[prefix + "_status_message"] = "Loading... {}/{} pts".format(done, total)
            request_expire(300, True)

        # Update previous states
        sc.sticky[prefix + "_prev_start"] = i_start
        sc.sticky[prefix + "_prev_stop"] = i_stop
        sc.sticky[prefix + "_prev_load"] = i_load

        # Output
        ghenv.Component.Message = sc.sticky[prefix + "_status_message"]  # noqa: F821
        return [sc.sticky[prefix + "_latest_cloud"]]