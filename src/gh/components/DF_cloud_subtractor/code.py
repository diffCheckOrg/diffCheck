from diffCheck import df_cvt_bindings as df_cvt

import Rhino
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

from ghpythonlib.componentbase import executingcomponent as component

class DFCloudSubtract(component):
    def __init__(self):
        super(DFCloudSubtract, self).__init__()
    def RunScript(self,
            i_cloud_subtract_from: Rhino.Geometry.PointCloud,
            i_cloud_subtract_with: Rhino.Geometry.PointCloud,
            i_distance_threshold: float):
        df_cloud = df_cvt.cvt_rhcloud_2_dfcloud(i_cloud_subtract_from)
        df_cloud_substract = df_cvt.cvt_rhcloud_2_dfcloud(i_cloud_subtract_with)
        if i_distance_threshold is None:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Distance threshold not defined. 0.01 used as default value.")# noqa: F821
            i_distance_threshold = 0.01
        if i_distance_threshold <= 0:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Distance threshold must be greater than 0. Please provide a valid distance threshold.")# noqa: F821
            return None
        df_cloud.subtract_points(df_cloud_substract, i_distance_threshold)
        rh_cloud = df_cvt.cvt_dfcloud_2_rhcloud(df_cloud)
        return [rh_cloud]
