"""Crops a point cloud by giving the bounding box or a brep."""
from diffCheck import df_cvt_bindings as df_cvt

import numpy as np

import Rhino
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

from ghpythonlib.componentbase import executingcomponent as component

TOL = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

class DFCloudCrop(component):
    def __init__(self):
        super(DFCloudCrop, self).__init__()

    def RunScript(self,
            i_cloud: Rhino.Geometry.PointCloud,
            i_box: Rhino.Geometry.Brep,
            i_brep: Rhino.Geometry.Brep):
        if i_cloud is None:
            ghenv.Component.AddRuntimeMessage(RML.Warning,"No point cloud provided. Please connect a point cloud to the input.")# noqa: F821
            return None

        if i_box is not None:
            bbox = i_box.GetBoundingBox(True)
            bb_min_as_array = np.asarray([bbox.Min.X, bbox.Min.Y, bbox.Min.Z])
            bb_max_as_array = np.asarray([bbox.Max.X, bbox.Max.Y, bbox.Max.Z])
            df_cloud = df_cvt.cvt_rhcloud_2_dfcloud(i_cloud)
            df_cloud_copy = df_cloud.duplicate()
            df_cloud.crop(bb_min_as_array, bb_max_as_array)
            df_cloud_copy.subtract_points(df_cloud, TOL)
            o_pts_out = df_cvt.cvt_dfcloud_2_rhcloud(df_cloud_copy)
            o_pts_in = df_cvt.cvt_dfcloud_2_rhcloud(df_cloud)

        elif i_brep is not None:
            pts_in =  []
            pts_out = []
            for pc_item in i_cloud:
                point = Rhino.Geometry.Point3d(pc_item.X, pc_item.Y, pc_item.Z)
                if i_brep.IsPointInside(point, TOL, True):
                    pts_in.append(point)
                else:
                    pts_out.append(point)
            o_pts_in = Rhino.Geometry.PointCloud(pts_in)
            o_pts_out = Rhino.Geometry.PointCloud(pts_out)

        else:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Please provide a box to crop the point cloud with") # noqa: F821

        return [o_pts_in, o_pts_out]
