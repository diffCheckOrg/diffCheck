#! python3


import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component


from diffCheck import df_cvt_bindings

class DFCloudSizeDownsample(component):
    def RunScript(self,
        i_cloud: rg.PointCloud,
        i_size: int,
    ) -> rg.PointCloud:
        df_cloud = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud)
        df_cloud.downsample_by_size(i_size)
        o_cloud = df_cvt_bindings.cvt_dfcloud_2_rhcloud(df_cloud)

        return [o_cloud]
