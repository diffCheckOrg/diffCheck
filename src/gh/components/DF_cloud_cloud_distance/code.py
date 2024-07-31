#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
from diffCheck import df_cvt_bindings
from diffCheck import df_error_estimation

import diffCheck.df_util


class CloudCloudDistance(component):
    def RunScript(self,
        i_cloud_source:  typing.List[rg.PointCloud],
        i_cloud_target: typing.List[rg.PointCloud],
        i_swap: bool):
        """
            The cloud-to-cloud component computes the distance between each point in the source point cloud and its nearest neighbour in thr target point cloud.

            :param i_cloud_source: a list of source point cloud
            :param i_cloud_target: a list of target point cloud to calculate distances to

            :return o_distances : list of calculated distances for each point
            :return o_rmse: the root mean squared error between corresponding points of source and target
            :return o_max_deviation: the max deviation between source and target
            :return o_min_deviation: the min deviation between source and target
            :return o_std_deviation: the standard deviation between source and target
            :returns o_resluts: the results of the comparison all in one object
        """

        if i_cloud_source is None or i_cloud_target is None:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Please provide both objects of type point clouds to compare")
            return None

        # swap
        if i_swap is True:
            temp = i_cloud_source
            i_cloud_source = i_cloud_target
            i_cloud_target = temp

        # conversion
        df_cloud_source_list = [df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cl_s) for i_cl_s in i_cloud_source]
        df_cloud_target_list = [df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cl_t) for i_cl_t in i_cloud_target]

        # calculate distances
        o_results = df_error_estimation.df_cloud_2_df_cloud_comparison(df_cloud_source_list, df_cloud_target_list)

        return o_results.distances, o_results.distances_rmse, o_results.distances_max_deviation, o_results.distances_min_deviation, o_results.distances_sd_deviation, o_results


# if __name__ == "__main__":
#     com = CloudCloudDistance()
#     o_distances, o_rmse, o_max_deviation, o_min_deviation, o_std_deviation, o_results = com.RunScript(
#         i_cloud_source,
#         i_cloud_target,
#         i_swap
#         )