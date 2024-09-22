#! python3

import System

import Rhino
from ghpythonlib.componentbase import executingcomponent as component
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
from diffCheck import df_cvt_bindings
from diffCheck import df_error_estimation


class DFCloudMeshDistance(component):
    def RunScript(self,
            i_cloud_source: System.Collections.Generic.List[Rhino.Geometry.PointCloud],
            i_assembly,
            i_signed_flag: bool,
            i_swap: bool,
            i_analysis_resolution: float):

        if i_analysis_resolution is None:
            scalef = diffCheck.df_util.get_doc_2_meters_unitf()
            i_analysis_resolution = 0.1 / scalef

        # Based on cloud source input + beam size, decide whether to calculate joints or entire assembly and output respective message
        if len(i_assembly.beams) == len(i_cloud_source):
            ghenv.Component.Message = "Per Beam"  # noqa: F821
            rh_mesh_target_list = [beam.to_mesh(i_analysis_resolution) for beam in i_assembly.beams]
        elif len(i_assembly.all_joints) == len(i_cloud_source):
            ghenv.Component.Message = "Per Joint"  # noqa: F821
            rh_mesh_target_list = [joint.to_mesh(i_analysis_resolution) for joint in i_assembly._all_joints]
        else:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "The input number of objects to compare matches neither the number of beams nor the number of joints")  # noqa: F821
            return None, None, None, None, None, None

        # conversion
        siffed_df_cloud_source_list = []
        siffed_rh_mesh_target_list = []
        for i in range(len(i_cloud_source)):
            if i_cloud_source[i] is not None:
                siffed_df_cloud_source_list.append(df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud_source[i]))
                siffed_rh_mesh_target_list.append(rh_mesh_target_list[i])


        # calculate distances
        o_result = df_error_estimation.df_cloud_2_rh_mesh_comparison(siffed_df_cloud_source_list, siffed_rh_mesh_target_list, i_signed_flag, i_swap)

        return o_result.distances, o_result.distances_rmse, o_result.distances_max_deviation, o_result.distances_min_deviation, o_result.distances_sd_deviation, o_result
