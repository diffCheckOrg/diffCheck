#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings
import diffCheck.df_util

class CloudToCloudDistance(component):
    def RunScript(self,
        i_cloud_source: rg.PointCloud,
        i_cloud_target: rg.PointCloud,
        
    ) -> [float]:
        """
            The cloud-to-cloud component computes the distance between each point in the source point cloud and its nearest neighbour in thr target point cloud.

            :param i_cloud_source: source point cloud
            :param i_cloud_target: target point cloud to align to

            :return o_distances : list of calculated distances for each point
        """
        if i_cloud_source is None or i_cloud_target is None:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Please provide both objects of type point clouds to compare")
            return None

        # conversion
        df_cloud_source = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud_source)
        df_cloud_target = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud_target)

        # calculate distances
        o_distances = cloud_2_cloud_distance(df_cloud_source, df_cloud_target)

        return o_distances


if __name__ == "__main__":
    com = CloudToCloudDistance(component)
    o_distances = com.RunScript(
        i_cloud_source,
        i_cloud_target
        )