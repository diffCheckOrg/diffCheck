#! python3

from ghpythonlib.componentbase import executingcomponent as component
import os
import tempfile
import requests
import threading
import Rhino
import Rhino.Geometry as rg
import scriptcontext as sc
from diffCheck import df_gh_canvas_utils


class DFHTTPListener(component):

    def __init__(self):
        try:
            ghenv.Component.ExpireSolution(True)  # noqa: F821
            ghenv.Component.Attributes.PerformLayout()  # noqa: F821
        except NameError:
            pass

        df_gh_canvas_utils.add_button(ghenv.Component, "Load", 0, x_offset=60)  # noqa: F821
        df_gh_canvas_utils.add_panel(ghenv.Component, "Ply_url", "https://github.com/diffCheckOrg/diffCheck/raw/refs/heads/main/tests/test_data/cube_mesh.ply", 1, 60, 20)  # noqa: F821

    def RunScript(self,
            i_load: bool,
            i_ply_url: str):

        prefix = 'http'

        # initialize sticky variables
        sc.sticky.setdefault(f'{prefix}_ply_url', None)  # last url processed
        sc.sticky.setdefault(f'{prefix}_imported_geom', None)  # last geo imported from ply
        sc.sticky.setdefault(f'{prefix}_status_message', "Waiting..")  # status message on component
        sc.sticky.setdefault(f'{prefix}_prev_load', False)  # previous state of toggle
        sc.sticky.setdefault(f'{prefix}_thread_running', False)  # is a background thread running?

        def _import_job(url):
            """
            Background job:
            - Downloads the .ply file from the URL
            - Imports it into the active Rhino document
            - Extracts the new geometry (point cloud or mesh)
            - Cleans up the temporary file and document objects
            - Updates sticky state and status message
            - Signals to GH that it should re-solve
            """

            tmp = None
            try:
                if not url.lower().endswith('.ply'):
                    raise ValueError("URL must end in .ply")

                resp = requests.get(url, timeout=30)
                resp.raise_for_status()
                # save om temporary file
                fn = os.path.basename(url)
                tmp = os.path.join(tempfile.gettempdir(), fn)
                with open(tmp, 'wb') as f:
                    f.write(resp.content)

                doc = Rhino.RhinoDoc.ActiveDoc
                # recordd existing object IDs to detect new ones
                before_ids = {o.Id for o in doc.Objects}

                # import PLY using Rhino's API
                opts = Rhino.FileIO.FilePlyReadOptions()
                ok = Rhino.FileIO.FilePly.Read(tmp, doc, opts)
                if not ok:
                    raise RuntimeError("Rhino.FilePly.Read failed")

                after_ids = {o.Id for o in doc.Objects}
                new_ids = after_ids - before_ids
                # get new pcd or mesh from document
                geom = None
                for guid in new_ids:
                    g = doc.Objects.FindId(guid).Geometry
                    if isinstance(g, rg.PointCloud):
                        geom = g.Duplicate()
                        break
                    elif isinstance(g, rg.Mesh):
                        geom = g.DuplicateMesh()
                        break
                # remove imported objects
                for guid in new_ids:
                    doc.Objects.Delete(guid, True)
                doc.Views.Redraw()

                # store new geometry
                sc.sticky[f'{prefix}_imported_geom'] = geom
                count = geom.Count if isinstance(geom, rg.PointCloud) else geom.Vertices.Count
                if isinstance(geom, rg.PointCloud):
                    sc.sticky[f'{prefix}_status_message'] = f"Loaded pcd with {count} pts"
                else:
                    sc.sticky[f'{prefix}_status_message'] = f"Loaded mesh wih {count} vertices"
                ghenv.Component.Message = sc.sticky.get(f'{prefix}_status_message')  # noqa: F821

            except Exception as e:
                sc.sticky[f'{prefix}_imported_geom'] = None
                sc.sticky[f'{prefix}_status_message'] = f"Error: {e}"
            finally:
                try:
                    os.remove(tmp)
                except Exception:
                    pass
                # mark thread as finished
                sc.sticky[f'{prefix}_thread_running'] = False
                ghenv.Component.ExpireSolution(True)  # noqa: F821

        # check if the URL input has changed
        if sc.sticky[f'{prefix}_ply_url'] != i_ply_url:
            sc.sticky[f'{prefix}_ply_url'] = i_ply_url
            sc.sticky[f'{prefix}_status_message'] = "URL changed. Press Load"
            sc.sticky[f'{prefix}_thread_running'] = False
            sc.sticky[f'{prefix}_prev_load'] = False

        # start importing if Load toggle is pressed and import thread is not already running
        if i_load and not sc.sticky[f'{prefix}_prev_load'] and not sc.sticky[f'{prefix}_thread_running']:
            sc.sticky[f'{prefix}_status_message'] = "Loading..."
            sc.sticky[f'{prefix}_thread_running'] = True
            threading.Thread(target=_import_job, args=(i_ply_url,), daemon=True).start()

        sc.sticky[f'{prefix}_prev_load'] = i_load
        ghenv.Component.Message = sc.sticky.get(f'{prefix}_status_message', "")  # noqa: F821

        # output
        o_geometry = sc.sticky.get(f'{prefix}_imported_geom')

        return [o_geometry]
