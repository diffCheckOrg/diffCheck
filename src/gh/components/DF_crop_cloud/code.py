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
            i_box: Rhino.Geometry.Brep,
            i_x_min: float,
            i_y_min: float,
            i_z_min: float,
            i_x_max: float,
            i_y_max: float,
            i_z_max: float):
        if i_cloud is None:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "No point cloud provided. Please connect a point cloud to the input.")  # noqa: F821
            return None

        if i_box is not None:
            bbox = i_box.GetBoundingBox(True)
            bb_min_as_array = np.asarray([bbox.Min.X, bbox.Min.Y, bbox.Min.Z])
            bb_max_as_array = np.asarray([bbox.Max.X, bbox.Max.Y, bbox.Max.Z])

            ghenv.Component.AddRuntimeMessage(RML.Remark, "A box is provided and is used to crop the point cloud, all other inputs neglected. To use min/max values, disconnect the box")  # noqa: F821
        else:
            if i_x_min is None:
                i_x_min = -np.inf
            if i_y_min is None:
                i_y_min = -np.inf
            if i_z_min is None:
                i_z_min = -np.inf
            if i_x_max is None:
                i_x_max = np.inf
            if i_y_max is None:
                i_y_max = np.inf
            if i_z_max is None:
                i_z_max = np.inf
            bb_min_as_array = np.asarray([i_x_min, i_y_min, i_z_min])
            bb_max_as_array = np.asarray([i_x_max, i_y_max, i_z_max])
        df_cloud = df_cvt.cvt_rhcloud_2_dfcloud(i_cloud)
        df_cloud.crop(bb_min_as_array, bb_max_as_array)
        rh_cloud = df_cvt.cvt_dfcloud_2_rhcloud(df_cloud)
        return [rh_cloud]
