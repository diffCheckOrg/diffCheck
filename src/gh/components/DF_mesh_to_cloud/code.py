#! python3

import System

import Rhino
from ghpythonlib.componentbase import executingcomponent as component


import diffCheck
import diffCheck.df_cvt_bindings



class DFMeshToCloud(component):
    def RunScript(self, i_mesh: Rhino.Geometry.Mesh, i_points: int) -> Rhino.Geometry.PointCloud:
        df_mesh = diffCheck.df_cvt_bindings.cvt_rhmesh_2_dfmesh(i_mesh)
        df_cloud = df_mesh.sample_points_uniformly(i_points)

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

        rgpoints = [Rhino.Geometry.Point3d(pt[0], pt[1], pt[2]) for pt in df_cloud.points]
        rh_cloud = Rhino.Geometry.PointCloud(rgpoints)

        return [rh_cloud]
