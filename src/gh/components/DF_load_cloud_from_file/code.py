#! python3

import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component


from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings

class DFLoadCloudFromFile(component):
    def RunScript(self,
        i_path: str,
        i_scalef: float) -> rg.PointCloud:
        if i_path is None:
            return None
        if i_scalef is None:
            i_scalef = 1.0

        df_cloud = diffcheck_bindings.dfb_geometry.DFPointCloud()
        df_cloud.load_from_PLY(i_path)
        rh_cloud = df_cvt_bindings.cvt_dfcloud_2_rhcloud(df_cloud)

        # scale  if needed
        centroid = rh_cloud.GetBoundingBox(True).Center
        x_form_scale = rg.Transform.Scale(centroid, i_scalef)
        rh_cloud.Transform(x_form_scale)

        return [rh_cloud]
