#! python3


import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component


import diffCheck
import diffCheck.df_cvt_bindings



class DFMeshToCloud(component):
    def RunScript(self,
            i_mesh: rg.Mesh,
            i_points: int) -> rg.PointCloud:
        df_mesh = diffCheck.df_cvt_bindings.cvt_rhmesh_2_dfmesh(i_mesh)
        df_cloud = df_mesh.sample_points_uniformly(i_points)

        # convert the df_cloud to a rhino cloud
        rgpoints = [rg.Point3d(pt[0], pt[1], pt[2]) for pt in df_cloud.points]
        rh_cloud = rg.PointCloud(rgpoints)

        return [rh_cloud]
