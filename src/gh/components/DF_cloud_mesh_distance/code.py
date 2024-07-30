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
from diffCheck.df_geometries import DFBeam


class CloudMeshDistance(component):
    def RunScript(self,
        i_cloud_source: typing.List[rg.PointCloud],
        i_beams: typing.List[DFBeam],
        i_signed_flag: bool,
        i_swap: bool,
        i_analysis_resolution):

        """
            The cloud-to-mesh component computes the distance between a point cloud and a mesh

            :param i_cloud_source: a list of point clouds
            :param i_beams: a list of DF beams
            :param i_signed_flag: calculate the sign of the distances
            :param i_swap: swap source and target

            :return o_distances : list of calculated distances for each point
            :return o_rmse: the root mean square error between corresponding points of source and target
            :return o_max_deviation: the max deviation between source and target
            :return o_min_deviation: the min deviation between source and target
            :returns o_results: the results of the comparison all in one object
        """
        if i_analysis_resolution is None:
            scalef = diffCheck.df_util.get_doc_2_meters_unitf()
            i_analysis_resolution = 0.1 / scalef

        # conversion
        df_cloud_source_list = [df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cl_s) for i_cl_s in i_cloud_source]
        df_mesh_target_list = [beam.to_mesh(i_analysis_resolution) for beam in i_beams]

        # calculate distances
        o_result = df_error_estimation.cloud_2_rhino_mesh_comparison(df_cloud_source_list, df_mesh_target_list, i_signed_flag, i_swap)

        return o_result.distances, o_result.distances_mse, o_result.distances_max_deviation, o_result.distances_min_deviation, o_result.distances_sd_deviation, o_result


# if __name__ == "__main__":
#     com = CloudMeshDistance()
#     o_distances, o_mse, o_max_deviation, o_min_deviation, o_std_deviation, o_results = com.RunScript(
#         i_cloud_source,
#         i_beams,
#         i_signed_flag,
#         i_swap,
#         i_analysis_resolution
#         )