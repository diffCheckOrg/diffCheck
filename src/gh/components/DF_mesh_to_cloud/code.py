#! python3

import System

import Rhino
from ghpythonlib.componentbase import executingcomponent as component


import diffCheck
import diffCheck.df_cvt_bindings



class DFMeshToCloud(component):
    def RunScript(self,
        i_meshes:System.Collections.Generic.IList[Rhino.Geometry.Mesh],
        i_points: int) -> Rhino.Geometry.PointCloud:

        if i_meshes is None:
            return None

        if i_points is None:
            i_points = 1000

        rh_mesh = i_meshes[0]
        for i  in range(1, len(i_meshes)):
            if i_meshes[i] is None:
                return None
            rh_mesh.Append(i_meshes[i])
        rh_mesh.Faces.ConvertQuadsToTriangles()

        df_mesh = diffCheck.df_cvt_bindings.cvt_rhmesh_2_dfmesh(rh_mesh)
        df_cloud = df_mesh.sample_points_uniformly(i_points)
        rgpoints = [Rhino.Geometry.Point3d(p[0], p[1], p[2]) for p in df_cloud.points]
        # convert the df_cloud to a rhino cloud
        rh_cloud = Rhino.Geometry.PointCloud(rgpoints)

        return [rh_cloud]
