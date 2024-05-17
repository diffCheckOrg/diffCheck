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


class DFGlobalRegistration(component):
    def RunScript(self,
        i_cloud_source: rg.PointCloud = None,
        i_cloud_target: rg.PointCloud = None
    ) -> rg.Transform:
        """
            The global registration component aligns two point clouds in a rough way.

            :param i_cloud_source: source point cloud
            :param i_cloud_target: target point cloud to align to

            :return o_x_form : transformation matrix
        """

        # if i_cloud_source is None or i_cloud_target is None:
        #     ghenv.Component.AddRuntimeMessage(RML.Error, "Please provide two point clouds to align")
        #     return o_x_form

        print(type(i_cloud_source))

        df_cloud_source = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud_source)
        df_cloud_target = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud_target)

        print(type(df_cloud_source))    
        # # print all the available registration methods
        # print(dir(diffcheck_bindings.dfb_registrations))
        # registrations = diffcheck_bindings.dfb_registrations.DFGlobalRegistrations()



        df_xform = diffcheck_bindings.dfb_registrations.DFGlobalRegistrations.O3DFastGlobalRegistrationFeatureMatching(
            source=df_cloud_source,
            target=df_cloud_target,
            voxelize=True,
            voxel_size=0.1,
            radius_kd_tree_search=0.1,
            max_neighbor_kd_tree_search=50,
            max_correspondence_distance=0.05,
            iteration_number=128,
            max_tuple_count=1000
        )
        print(type(df_xform))

        print(df_xform.transformation_matrix)
        print("-------------------")
        print(df_xform.rotation_matrix)
        print("-------------------")
        print(df_xform.translation_vector)

        df_xform_matrix = df_xform.transformation_matrix


        rh_form = rg.Transform()
        for i in range(4):
            for j in range(4):
                rh_form[i, j] = df_xform_matrix[i, j]

        print(rh_form)

        o_x_form = rh_form


        return o_x_form


if __name__ == "__main__":
    com = DFGlobalRegistration()
    o_x_form = com.RunScript(i_cloud_source, i_cloud_target)