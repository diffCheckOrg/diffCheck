"""Merges point clouds together."""
import diffCheck
from diffCheck.diffcheck_bindings import dfb_geometry as df_geometry
import Rhino

import System

from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

from ghpythonlib.componentbase import executingcomponent as component

TOL = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

class DFMergeAssemblies(component):
    def RunScript(self,
            i_clouds: System.Collections.Generic.List[Rhino.Geometry.PointCloud]):
        if i_clouds is None or len(i_clouds) == 0:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "No point clouds provided. Please connect point clouds to the input.") # noqa: F821
            return None

        merged_cloud = df_geometry.DFPointCloud()
        for cloud in i_clouds:
            df_cloud = diffCheck.df_cvt_bindings.cvt_rhcloud_2_dfcloud(cloud)
            merged_cloud.add_points(df_cloud)

        o_cloud =  diffCheck.df_cvt_bindings.cvt_dfcloud_2_rhcloud(merged_cloud)
        return [o_cloud]
