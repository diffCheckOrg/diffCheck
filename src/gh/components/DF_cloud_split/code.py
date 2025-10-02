"""Crops a point cloud by giving the bounding box or a brep."""
from diffCheck import df_cvt_bindings as df_cvt

import numpy as np

import Rhino

from ghpythonlib.componentbase import executingcomponent as component

TOL = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

class DFCloudSplit(component):
    def __init__(self):
        super(DFCloudSplit, self).__init__()

    def RunScript(self,
            i_cloud: Rhino.Geometry.PointCloud,
            i_boundary: Rhino.Geometry.Brep):

        if i_boundary.IsBox():
            vertices = i_boundary.Vertices
            bb_as_array = [np.asarray([vertice.Location.X, vertice.Location.Y, vertice.Location.Z]) for vertice in vertices]
            df_cloud = df_cvt.cvt_rhcloud_2_dfcloud(i_cloud)
            df_cloud_copy = df_cloud.duplicate()
            df_cloud.crop(bb_as_array)
            df_cloud_copy.subtract_points(df_cloud, TOL)
            o_pts_out = df_cvt.cvt_dfcloud_2_rhcloud(df_cloud_copy)
            o_pts_in = df_cvt.cvt_dfcloud_2_rhcloud(df_cloud)

        else:
            pts_in = []
            pts_out = []
            for pc_item in i_cloud:
                point = Rhino.Geometry.Point3d(pc_item.X, pc_item.Y, pc_item.Z)
                if i_boundary.IsPointInside(point, TOL, True):
                    pts_in.append(point)
                else:
                    pts_out.append(point)
            o_pts_in = Rhino.Geometry.PointCloud(pts_in)
            o_pts_out = Rhino.Geometry.PointCloud(pts_out)

        return [o_pts_in, o_pts_out]
