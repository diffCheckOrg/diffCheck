#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
import diffCheck.df_geometries
from diffCheck import df_cvt_bindings

class DFCloudVoxelDownsample(component):
    def RunScript(self,
        i_cloud: rg.PointCloud,
        i_voxel_size: float,
    ) -> rg.PointCloud:
        """
            Downsample a point cloud using a voxel grid filter.

            :param i_cloud: input point cloud
            :param i_voxel_size: voxel size, the value represents the side of the voxel

            :return o_cloud: downsampled point cloud
        """
        df_cloud = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud)
        df_cloud.voxel_downsample(i_voxel_size)
        o_cloud = df_cvt_bindings.cvt_dfcloud_2_rhcloud(df_cloud)

        return o_cloud

# if __name__ == "__main__":
#     com = DFCloudVoxelDownsample()
#     o_cloud = com.RunScript(
#         i_cloud,
#         i_voxel_size,
#         )