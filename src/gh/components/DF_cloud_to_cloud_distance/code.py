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
from diffCheck import df_error_estimation

import diffCheck.df_util


class CloudToCloudDistance(component):
    def RunScript(self,
        i_cloud_source: rg.PointCloud,
        i_cloud_target: rg.PointCloud,
        i_signed_flag: bool):
        """
            The cloud-to-cloud component computes the distance between each point in the source point cloud and its nearest neighbour in thr target point cloud.

            :param i_cloud_source: source point cloud
            :param i_cloud_target: target point cloud to align to
            :param i_signed_flag: whether to take normals into account

            :return o_distances : list of calculated distances for each point
            :return o_mse: the average squared difference between corresponding points of source and target
            :return o_max_deviation: the max deviation between source and target (Hausdorff Distance)
            :return o_min_deviation: the min deviation between source and target
            :return o_std_deviation: the standard deviation between source and target
        """
        if i_cloud_source is None or i_cloud_target is None:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Please provide both objects of type point clouds to compare")
            return None
        
        if i_signed_flag and not i_cloud_target.ContainsNormals:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Please provide a target point cloud with normals or assign false to i_signed_flag")
            return None

        # conversion
        df_cloud_source = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud_source)
        df_cloud_target = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud_target)

        # calculate distances
        o_distances = df_error_estimation.cloud_2_cloud_distance(df_cloud_source, df_cloud_target, i_signed_flag)
        o_mse = df_error_estimation.compute_mse(o_distances)
        o_max_deviation = df_error_estimation.compute_max_deviation(o_distances)
        o_min_deviation = df_error_estimation.compute_min_deviation(o_distances)
        o_std_deviation = df_error_estimation.compute_standard_deviation(o_distances)

        return o_distances.tolist(), o_mse, o_max_deviation, o_min_deviation, o_std_deviation


if __name__ == "__main__":
    com = CloudToCloudDistance()
    o_distances, o_mse, o_max_deviation, o_min_deviation, o_std_deviation = com.RunScript(
        i_cloud_source,
        i_cloud_target,
        i_signed_flag
        )