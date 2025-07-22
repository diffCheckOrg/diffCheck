from diffCheck import df_cvt_bindings as df_cvt

import numpy as np

import Rhino
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

from ghpythonlib.componentbase import executingcomponent as component

class DFCloudCrop(component):
    def __init__(self):
        super(DFCloudCrop, self).__init__()
    def RunScript(self,
            i_cloud: Rhino.Geometry.PointCloud,
            i_box: Rhino.Geometry.Brep):
        if i_cloud is None:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "No point cloud provided. Please connect a point cloud to the input.")  # noqa: F821
            return None

        if i_box is not None:
            bbox = i_box.GetBoundingBox(True)
            bb_min_as_array = np.asarray([bbox.Min.X, bbox.Min.Y, bbox.Min.Z])
            bb_max_as_array = np.asarray([bbox.Max.X, bbox.Max.Y, bbox.Max.Z])

        else:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Please provide a box to crop the point cloud with")  # noqa: F821

        df_cloud = df_cvt.cvt_rhcloud_2_dfcloud(i_cloud)
        df_cloud.crop(bb_min_as_array, bb_max_as_array)
        rh_cloud = df_cvt.cvt_dfcloud_2_rhcloud(df_cloud)
        return [rh_cloud]
