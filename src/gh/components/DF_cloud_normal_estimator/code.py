#! python3

import System

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import diffCheck
import diffCheck.df_geometries
from diffCheck import df_cvt_bindings

class DFCloudNormalEstimator(component):
    def RunScript(self,
        i_cloud : rg.PointCloud = None,
        i_knn : int = None,
        i_radius : float = None,
        i_switch_mode : bool = True
    ):
        o_cloud = rg.PointCloud()

        df_cloud = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud)

        if i_knn is None:
            i_knn = 100

        df_cloud.estimate_normals(
            use_cilantro_evaluator=i_switch_mode,
            knn=i_knn,
            search_radius=i_radius
            )

        o_cloud = df_cvt_bindings.cvt_dfcloud_2_rhcloud(df_cloud)

        return o_cloud
