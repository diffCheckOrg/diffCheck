#! python3


import Rhino
from ghpythonlib.componentbase import executingcomponent as component


from diffCheck import df_cvt_bindings

class DFCloudUniformDownsample(component):
    def RunScript(self, i_cloud: Rhino.Geometry.PointCloud, i_every_k_points: int) -> Rhino.Geometry.PointCloud:
        df_cloud = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud)
        df_cloud.uniform_downsample(i_every_k_points)
        o_cloud = df_cvt_bindings.cvt_dfcloud_2_rhcloud(df_cloud)

        return [o_cloud]
