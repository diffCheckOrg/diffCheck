#! python3

import Rhino
from ghpythonlib.componentbase import executingcomponent as component

from diffCheck import df_cvt_bindings

class DFCloudNormalEstimator(component):
    def RunScript(self,
            i_cloud: Rhino.Geometry.PointCloud,
            i_knn: int,
            i_radius: int,
            i_switch_mode: bool):
        o_cloud = Rhino.Geometry.PointCloud()

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
