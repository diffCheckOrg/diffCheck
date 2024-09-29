"""Computes the distance between a point cloud and a mesh"""
#! python3
# r: diffCheck==1.0.0

import Rhino
import Grasshopper
from ghpythonlib.componentbase import executingcomponent as component
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
from diffCheck import df_cvt_bindings
from diffCheck import df_error_estimation


class DFCloudMeshDistance(component):

    def RunScript(self,
        i_cloud_source: Grasshopper.DataTree[Rhino.Geometry.PointCloud],
        i_assembly,
        i_signed_flag: bool,
        i_swap: bool,
        i_analysis_resolution: float):

        if i_cloud_source is None or i_assembly is None:
            return None, None, None, None, None, None

        if i_analysis_resolution is None:
            scalef = diffCheck.df_util.get_doc_2_meters_unitf()
            i_analysis_resolution = 0.1 / scalef

        # if the input is Gh tree, flatten it
        flat_list = []
        for branch in i_cloud_source.Branches:
            flat_list.extend(list(branch))
        i_cloud_list = flat_list

        # Based on cloud source input + beam size, decide whether to calculate joints or entire assembly and output respective message
        if len(i_assembly.beams) == len(i_cloud_list):
            ghenv.Component.Message = "Per Beam"  # noqa: F821
            rh_mesh_target_list = [beam.to_mesh(i_analysis_resolution) for beam in i_assembly.beams]
        elif len(i_assembly.all_joints) == len(i_cloud_list):
            ghenv.Component.Message = "Per Joint"  # noqa: F821
            rh_mesh_target_list = [joint.to_mesh(i_analysis_resolution) for joint in i_assembly._all_joints]
        elif len(i_assembly.all_joint_faces) == len(i_cloud_list):
            ghenv.Component.Message = "Per Joint Face"  # noqa: F821
            rh_mesh_target_list = [joint_face.to_mesh() for joint_face in i_assembly.all_joint_faces]
        else:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "The input number of objects to compare matches neither the number of beams nor the number of joints")  # noqa: F821
            return None, None, None, None, None, None

        #conversion to DFCloud
        df_cloud_source_list = [df_cvt_bindings.cvt_rhcloud_2_dfcloud(rh_cloud) for rh_cloud in i_cloud_list]

        # calculate distances
        o_result = df_error_estimation.df_cloud_2_rh_mesh_comparison(i_assembly, df_cloud_source_list, rh_mesh_target_list, i_signed_flag, i_swap)  # noqa: F821

        # distances to tree
        distances_tree = Grasshopper.DataTree[object]()
        for i, sublist in enumerate(o_result.distances):
            for j, item in enumerate(sublist):
                path = Grasshopper.Kernel.Data.GH_Path(i)
                distances_tree.Add(item, path)

        return distances_tree, o_result.distances_rmse, o_result.distances_max_deviation, o_result.distances_min_deviation, o_result.distances_sd_deviation, o_result
