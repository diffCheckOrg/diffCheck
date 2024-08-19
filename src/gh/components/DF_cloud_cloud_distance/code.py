#! python3

import typing

import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

from diffCheck import df_cvt_bindings
from diffCheck import df_error_estimation



class DFCloudCloudDistance(component):
    def RunScript(self,
        i_cloud_source:  typing.List[rg.PointCloud],
        i_cloud_target: typing.List[rg.PointCloud],
        i_swap: bool):
        if i_cloud_source is None or i_cloud_target is None:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Please provide both objects of type point clouds to compare")  # noqa: F821
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
