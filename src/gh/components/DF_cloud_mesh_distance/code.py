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


class DFCloudMeshDistance(component):
    def RunScript(self,
        i_cloud_source: typing.List[rg.PointCloud],
        i_beams: typing.List[DFBeam],
        i_signed_flag: bool,
        i_swap: bool,
        i_analysis_resolution):

        if i_analysis_resolution is None:
            scalef = diffCheck.df_util.get_doc_2_meters_unitf()
            i_analysis_resolution = 0.1 / scalef

        # conversion
        df_cloud_source_list = [df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cl_s) for i_cl_s in i_cloud_source]
        rh_mesh_target_list = [beam.to_mesh(i_analysis_resolution) for beam in i_beams]

        # calculate distances
        o_result = df_error_estimation.df_cloud_2_rh_mesh_comparison(df_cloud_source_list, rh_mesh_target_list, i_signed_flag, i_swap)

        return o_result.distances, o_result.distances_rmse, o_result.distances_max_deviation, o_result.distances_min_deviation, o_result.distances_sd_deviation, o_result