#! python3


import Rhino
from ghpythonlib.componentbase import executingcomponent as component

from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings


class DFRANSACGlobalRegistration(component):
    def RunScript(self,
        i_cloud_source: Rhino.Geometry.PointCloud,
        i_cloud_target: Rhino.Geometry.PointCloud,
        i_radius_kd_search: float,
        i_neighbours_kd_search: int,
        i_max_corrspondence_dist: float,
        is_t_estimate_pt2pt: bool,
        i_ransac_n: int,
        i_checker_dist: float,
        i_similarity_threshold: float,
        i_max_iterations: int,
        i_confidence_threshold: float
    ) -> Rhino.Geometry.Transform:
        if i_cloud_source is None or i_cloud_target is None:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Please provide both objects of type point clouds to align")  # noqa: F821
            return None
        if not i_cloud_source.ContainsNormals or not i_cloud_target.ContainsNormals:
            ghenv.Component.AddRuntimeMessage(RML.Error, "Please compute cloud's normals with a component before")  # noqa: F821

        # set default values
        if i_radius_kd_search is None:
            i_radius_kd_search = 1
        if i_neighbours_kd_search is None:
            i_neighbours_kd_search = 50
        if i_max_corrspondence_dist is None:
            i_max_corrspondence_dist = 0.5
        if is_t_estimate_pt2pt is None:
            is_t_estimate_pt2pt = False
        if i_ransac_n is None:
            i_ransac_n = 3
        if i_checker_dist is None:
            i_checker_dist = 0.5
        if i_similarity_threshold is None:
            i_similarity_threshold = 1.5
        if i_max_iterations is None:
            i_max_iterations = 5000
        if i_confidence_threshold is None:
            i_confidence_threshold = 0.999

        # conversion
        df_cloud_source = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud_source)
        df_cloud_target = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud_target)

        # fast registration
        df_xform = diffcheck_bindings.dfb_registrations.DFGlobalRegistrations.O3DRansacOnFeatureMatching(
            source=df_cloud_source,
            target=df_cloud_target,
            voxelize=False,  # set as default
            voxel_size=0.1,  # set as default
            radius_kd_tree_search=i_radius_kd_search,
            max_neighbor_kd_tree_search=i_neighbours_kd_search,
            max_correspondence_distance=i_max_corrspondence_dist,
            is_t_estimate_pt2pt=is_t_estimate_pt2pt,
            ransac_n=i_ransac_n,
            correspondence_checker_distance=i_checker_dist,
            similarity_threshold=i_similarity_threshold,
            ransac_max_iteration=i_max_iterations,
            ransac_confidence_threshold=i_confidence_threshold
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
