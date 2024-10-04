#! python3

import System
import Rhino
from ghpythonlib.componentbase import executingcomponent as component
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
import ghpythonlib.treehelpers as th

import diffCheck
from diffCheck import df_error_estimation


class DFCloudMeshDistance(component):

    def RunScript(self,
            i_cloud_source: System.Collections.Generic.List[Rhino.Geometry.PointCloud],
            i_assembly,
            i_signed_flag: bool,
            i_swap: bool,
            i_analysis_resolution: float):

        if i_cloud_source is None or i_assembly is None:
            return None, None, None, None, None, None

        if i_analysis_resolution is None:
            scalef = diffCheck.df_util.get_doc_2_meters_unitf()
            i_analysis_resolution = 0.1 / scalef

        if len(i_assembly.beams) == len(i_cloud_source):
            ghenv.Component.Message = "Per Beam"  # noqa: F821
            rh_mesh_target_list = [beam.to_mesh(i_analysis_resolution) for beam in i_assembly.beams]
        elif len(i_assembly.all_joints) == len(i_cloud_source):
            ghenv.Component.Message = "Per Joint"  # noqa: F821
            rh_mesh_target_list = [joint.to_mesh(i_analysis_resolution) for joint in i_assembly._all_joints]
        elif len(i_assembly.all_joint_faces) == len(i_cloud_source):
            ghenv.Component.Message = "Per Joint Face"  # noqa: F821
            rh_mesh_target_list = []
            for joint in i_assembly._all_joints:
                for face in joint.faces:
                    rh_mesh_target_list.append(face.to_mesh())
        else:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "The input number of objects to compare matches neither the number of beams nor the number of joints")  # noqa: F821
            return None, None, None, None, None, None

        o_result = df_error_estimation.rh_cloud_2_rh_mesh_comparison(
            i_assembly,
            i_cloud_source,
            rh_mesh_target_list,
            i_signed_flag,
            i_swap)  # noqa: F821

        distances_gh_tree = th.list_to_tree(o_result.distances)

        return distances_gh_tree, o_result.distances_mean, o_result.distances_rmse, o_result.distances_max_deviation, o_result.distances_min_deviation, o_result.distances_sd_deviation, o_result
