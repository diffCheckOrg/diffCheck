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

class DFCloudUniformDownsample(component):
    def RunScript(self,
        i_cloud: rg.PointCloud,
        i_every_k_points: int,
    ) -> rg.PointCloud:
        """
            Downsample a point cloud using in a uniform way by selecting every k points to delete.

            :param i_cloud: input point cloud
            :param i_every_k_points: number of every k points to delete

            :return o_cloud: downsampled point cloud
        """
        df_cloud = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud)
        df_cloud.uniform_downsample(i_every_k_points)
        o_cloud = df_cvt_bindings.cvt_dfcloud_2_rhcloud(df_cloud)

        return o_cloud

# if __name__ == "__main__":
#     com = DFCloudUniformDownsample()
#     o_cloud = com.RunScript(
#         i_cloud,
#         i_every_k_points,
#         )