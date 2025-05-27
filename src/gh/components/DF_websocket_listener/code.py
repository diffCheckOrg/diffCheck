#! python3

from ghpythonlib.componentbase import executingcomponent as component
import os
import tempfile
import requests
import threading
import Rhino
import Rhino.Geometry as rg
import scriptcontext as sc


class DFHTTPListener(component):

    def RunScript(self,
            i_load: bool,
            i_ply_url: str):

        sc.sticky.setdefault('ply_url', None)
        sc.sticky.setdefault('imported_geom', None)
        sc.sticky.setdefault('status_message','Idle')
        sc.sticky.setdefault('prev_load', False)
        sc.sticky.setdefault('thread_running', False)

        def _import_job(url):
            try:
                if not url.lower().endswith('.ply'):
                    raise ValueError("URL must end in .ply")

                resp = requests.get(url, timeout=30)
                resp.raise_for_status()
                fn = os.path.basename(url)
                tmp = os.path.join(tempfile.gettempdir(), fn)
                with open(tmp, 'wb') as f:
                    f.write(resp.content)

                doc = Rhino.RhinoDoc.ActiveDoc
                before_ids = {o.Id for o in doc.Objects}

                opts = Rhino.FileIO.FilePlyReadOptions()
                ok = Rhino.FileIO.FilePly.Read(tmp, doc, opts)
                if not ok:
                    raise RuntimeError("Rhino.FilePly.Read failed")

                after_ids = {o.Id for o in doc.Objects}
                new_ids = after_ids - before_ids

                geom = None
                for guid in new_ids:
                    g = doc.Objects.FindId(guid).Geometry
                    if isinstance(g, rg.PointCloud):
                        geom = g.Duplicate()
                        break
                    elif isinstance(g, rg.Mesh):
                        geom = g.DuplicateMesh()
                        break

                for guid in new_ids:
                    doc.Objects.Delete(guid, True)
                doc.Views.Redraw()

                sc.sticky['imported_geom']  = geom
                count = geom.Count if isinstance(geom, rg.PointCloud) else geom.Vertices.Count
                if isinstance(geom, rg.PointCloud):
                    sc.sticky['status_message'] = f"Done: {count} points"
                else:
                    sc.sticky['status_message'] = f"Done: {count} vertices"
                ghenv.Component.Message = sc.sticky.get('status_message')  # noqa: F821

            except Exception as e:
                sc.sticky['imported_geom'] = None
                sc.sticky['status_message'] = f"Error: {e}"
            finally:
                try:
                    os.remove(tmp)
                except Exception:
                    pass
                sc.sticky['thread_running'] = False
                ghenv.Component.ExpireSolution(True)  # noqa: F821

        if sc.sticky['ply_url'] != i_ply_url:
            sc.sticky['ply_url'] = i_ply_url
            sc.sticky['status_message'] = "URL changed. Press Load"
            sc.sticky['thread_running'] = False
            sc.sticky['prev_load'] = False

        if i_load and not sc.sticky['prev_load'] and not sc.sticky['thread_running']:
            sc.sticky['status_message'] = "Loading..."
            sc.sticky['thread_running'] = True
            threading.Thread(target=_import_job, args=(i_ply_url,), daemon=True).start()

        sc.sticky['prev_load'] = i_load
        ghenv.Component.Message = sc.sticky.get('status_message', "")  # noqa: F821

        # output
        o_geometry = sc.sticky.get('imported_geom')

        return [o_geometry]
