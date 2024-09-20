#! python3


import Rhino
from ghpythonlib.componentbase import executingcomponent as component

from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings


class DFICPRegistration(component):
    def RunScript(self,
            i_use_generalized_icp: bool,
            i_cloud_source: Rhino.Geometry.PointCloud,
            i_cloud_target: Rhino.Geometry.PointCloud,
            i_max_corrspondence_dist: float,
            i_max_iteration: int,
            is_t_estimate_pt2pt: bool,
            i_use_point_to_plane: bool) -> Rhino.Geometry.Transform:
        if i_cloud_source is None or i_cloud_target is None:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Please provide both objects of type point clouds to align")  # noqa: F821
            return None
        if not i_cloud_source.ContainsNormals or not i_cloud_target.ContainsNormals:
            ghenv.Component.AddRuntimeMessage(RML.Error, "Please compute cloud's normals with a component before")  # noqa: F821

        # set default values
        if i_use_generalized_icp is None:
            i_use_generalized_icp = True
        if i_max_corrspondence_dist is None:
            i_max_corrspondence_dist = 5
        if i_max_iteration is None:
            i_max_iteration = 50

        # conversion
        df_cloud_source = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud_source)
        df_cloud_target = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud_target)

        # fast registration
        # these are the only hardcoded values since it will get the best result
        RELATIVE_FITNESS = 1e-6
        RELATIVE_RMSE = 1e-6

        df_xform = None
        if i_use_generalized_icp:
            df_xform = diffcheck_bindings.dfb_registrations.DFRefinedRegistration.O3DGeneralizedICP(
                source=df_cloud_source,
                target=df_cloud_target,
                max_correspondence_distance=i_max_corrspondence_dist,
                max_iteration=i_max_iteration,
                relative_fitness=RELATIVE_FITNESS,
                relative_rmse=RELATIVE_RMSE
            )
        else:
            df_xform = diffcheck_bindings.dfb_registrations.DFRefinedRegistration.O3DICP(
                source=df_cloud_source,
                target=df_cloud_target,
                max_correspondence_distance=i_max_corrspondence_dist,
                is_t_estimate_pt2pt=is_t_estimate_pt2pt,
                relative_fitness=RELATIVE_FITNESS,
                relative_rmse=RELATIVE_RMSE,
                max_iteration=i_max_iteration,
                use_point_to_plane=i_use_point_to_plane
            )
        print("-------------------")
        print("Estimated transformation matrix:")
        print(df_xform.transformation_matrix)
        print("-------------------")

        # cvt df xform to rhino xform
        df_xform_matrix = df_xform.transformation_matrix
        rh_form = Rhino.Geometry.Transform()
        for i in range(4):
            for j in range(4):
                rh_form[i, j] = df_xform_matrix[i, j]
        if rh_form == Rhino.Geometry.Transform.Identity:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "The transformation matrix is identity, no transformation is applied")  # noqa: F821
            return None

        o_x_form = rh_form

        return o_x_form
