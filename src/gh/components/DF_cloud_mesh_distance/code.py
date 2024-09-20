#! python3

import typing
import System
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
from System.Windows.Forms import ToolStripSeparator

import diffCheck
from diffCheck import df_cvt_bindings
from diffCheck import df_error_estimation
from diffCheck.df_geometries import DFAssembly


class DFCloudMeshDistance(component):

    def RunScript(self,
        i_cloud_source: typing.List[rg.PointCloud],
        i_assembly: DFAssembly,
        i_signed_flag: bool,
        i_swap: bool,
        i_analysis_resolution):

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
        elif len(i_assembly.all_joint_faces) == len(i_cloud_source):
            ghenv.Component.Message = "Per Joint Face"  # noqa: F821
            rh_mesh_target_list = [joint_face.to_mesh(i_analysis_resolution) for joint_face in i_assembly._all_joint_faces]
        else:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "The input number of objects to compare matches neither the number of beams nor the number of joints")  # noqa: F821
            return None, None, None, None, None, None

        # conversion
        df_cloud_source_list = [df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cl_s) for i_cl_s in i_cloud_source]

        # calculate distances
        o_result = df_error_estimation.df_cloud_2_rh_mesh_comparison(df_cloud_source_list, rh_mesh_target_list, i_signed_flag, i_swap)

        return o_result.distances, o_result.distances_rmse, o_result.distances_max_deviation, o_result.distances_min_deviation, o_result.distances_sd_deviation, o_result

# if __name__ == "__main__":
#     com = DFCloudMeshDistance()
#     o_viz_settings = com.RunScript(
#         i_cloud_source,
#         i_assembly,
#         i_signed_flag,
#         i_swap,
#         i_analysis_resolution
#         )