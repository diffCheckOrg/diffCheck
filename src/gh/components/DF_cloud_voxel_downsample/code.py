#! python3


import Rhino
from ghpythonlib.componentbase import executingcomponent as component


from diffCheck import df_cvt_bindings

class DFCloudVoxelDownsample(component):
    def RunScript(self,
        i_cloud: Rhino.Geometry.PointCloud,
        i_voxel_size: float) -> Rhino.Geometry.PointCloud:
        if i_cloud is None or i_voxel_size is None:
            return None
        df_cloud = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud)
        df_cloud.voxel_downsample(i_voxel_size)
        o_cloud = df_cvt_bindings.cvt_dfcloud_2_rhcloud(df_cloud)

        return [o_cloud]
