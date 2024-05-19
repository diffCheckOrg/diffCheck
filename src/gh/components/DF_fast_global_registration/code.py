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


class DFFastGlobalRegistration(component):
    def RunScript(self,
        i_cloud_source: rg.PointCloud,
        i_cloud_target: rg.PointCloud,
        i_radius_kd_search: float,
        i_neighbours_kd_search: int,
        i_max_corrspondence_dist: float,
        i_iteration_number: int,
        i_max_tuple_count: int
    ) -> rg.Transform:
        """
            The global registration component aligns two point clouds in a rough way.

            :param i_cloud_source: source point cloud
            :param i_cloud_target: target point cloud to align to
            :param i_radius_kd_search: radius for the kd search
            :param i_neighbours_kd_search: number of neighbours to consider
            :param i_max_corrspondence_dist: maximum correspondence distance
            :param i_iteration_number: number of iterations
            :param i_max_tuple_count: maximum tuple count

            :return o_x_form : transformation matrix
        """
        if i_cloud_source is None or i_cloud_target is None:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Please provide both objects of type point clouds to align")
            return None

        # set default values
        if i_radius_kd_search is None: i_radius_kd_search = 0.8
        if i_neighbours_kd_search is None: i_neighbours_kd_search = 50
        if i_max_corrspondence_dist is None: i_max_corrspondence_dist = 0.05
        if i_iteration_number is None: i_iteration_number = 128
        if i_max_tuple_count is None: i_max_tuple_count = 1000

        # get the working unit of the Rhino document, if other than meters, set a multiplier factor
        scalef = diffCheck.df_util.get_doc_2_meters_unitf()
        i_radius_kd_search *= scalef
        i_max_corrspondence_dist *= scalef

        df_cloud_source = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud_source)
        df_cloud_target = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud_target)

        df_xform = diffcheck_bindings.dfb_registrations.DFGlobalRegistrations.O3DFastGlobalRegistrationFeatureMatching(
            source=df_cloud_source,
            target=df_cloud_target,
            voxelize=False,  # set as default
            voxel_size=0.1,  # set as default
            radius_kd_tree_search=i_radius_kd_search,
            max_neighbor_kd_tree_search=i_neighbours_kd_search,
            max_correspondence_distance=i_max_corrspondence_dist,
            iteration_number=i_iteration_number,
            max_tuple_count=i_max_tuple_count
        )
        print("-------------------")
        print("Estimated transformation matrix:")
        print(df_xform.transformation_matrix)
        print("-------------------")

        # cvt df xform to rhino xform
        df_xform_matrix = df_xform.transformation_matrix
        rh_form = rg.Transform()
        for i in range(4):
            for j in range(4):
                rh_form[i, j] = df_xform_matrix[i, j]
        if rh_form == rg.Transform.Identity:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "The transformation matrix is identity, no transformation is applied")
            return None

        o_x_form = rh_form

        return o_x_form


# if __name__ == "__main__":
#     com = DFFastGlobalRegistration()
#     o_x_form = com.RunScript(
#         i_cloud_source,
#         i_cloud_target,
#         i_radius_kd_search,
#         i_neighbours_kd_search,
#         i_max_corrspondence_dist,
#         i_iteration_number,
#         i_max_tuple_count
#         )