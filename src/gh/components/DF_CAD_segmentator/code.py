#! python3

import System

import Rhino
from ghpythonlib.componentbase import executingcomponent as component
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
import ghpythonlib.treehelpers as th


from diffCheck.diffcheck_bindings import dfb_segmentation
from diffCheck.diffcheck_bindings import dfb_geometry, dfb_registrations

from diffCheck import df_cvt_bindings



class DFCADSegmentator(component):
    def RunScript(self,
            i_clouds: System.Collections.Generic.List[Rhino.Geometry.PointCloud],
            i_assembly,
            i_angle_threshold: float,
            i_association_threshold: float,
            i_maximum_face_segment_distance: float,
            i_radius_normal_estimation: float,
            i_max_correspondence_distance_icp: float):

        if i_clouds is None or i_assembly is None:
            self.AddRuntimeMessage(RML.Warning, "Please provide a cloud and an assembly to segment.")
            return None
        if i_angle_threshold is None:
            i_angle_threshold = 0.1
        if i_association_threshold is None:
            i_association_threshold = 0.1
        if i_radius_normal_estimation is None:
            i_radius_normal_estimation = 0.01
        o_face_clusters = []
        o_transforms = []
        df_clusters = []
        # we make a deepcopy of the input clouds
        df_clouds = [df_cvt_bindings.cvt_rhcloud_2_dfcloud(cloud.Duplicate()) for cloud in i_clouds]
        df_merged_cloud = dfb_geometry.DFPointCloud()
        df_merged_cloud.remove_statistical_outliers(100, 1.5)
        for pc in df_clouds:
            df_merged_cloud.add_points(pc)

        df_beams = i_assembly.beams

        rh_meshes = []
        for i, df_b in enumerate(df_beams):
            rh_b_mesh_faces = [df_b_f.to_mesh() for df_b_f in df_b.side_faces]
            for df_j_face in df_b.joint_faces:
                rh_b_mesh_faces.append(df_j_face.to_mesh())
            rh_mesh = Rhino.Geometry.Mesh()
            for rh_b_mesh_face in rh_b_mesh_faces:
                rh_mesh.Append(rh_b_mesh_face)

            df_b_mesh = df_cvt_bindings.cvt_rhmesh_2_dfmesh(rh_mesh)
            df_sampled_cloud = df_b_mesh.sample_points_uniformly(1000)
            df_sampled_cloud.estimate_normals(use_cilantro_evaluator=False,
            search_radius = i_radius_normal_estimation,
            )

            transform = dfb_registrations.DFRefinedRegistration.O3DICP(
                source=df_sampled_cloud,
                target=df_merged_cloud,
                max_correspondence_distance= i_max_correspondence_distance_icp,
                max_iteration = 1000
                )

            df_xform = transform.transformation_matrix
            rh_xform = Rhino.Geometry.Transform()
            for i in range(4):
                for j in range(4):
                    rh_xform[i, j] = df_xform[i, j]
            o_transforms.append(rh_xform)

        df_asssociated_cluster_faces_per_beam = []
        for i, df_b in enumerate(df_beams):
            rh_b_mesh_faces = [df_b_f.to_mesh() for df_b_f in df_b.side_faces]
            rh_test_mesh = Rhino.Geometry.Mesh()
            for j in range(len(rh_b_mesh_faces)):
                sucess = rh_b_mesh_faces[j].Transform(o_transforms[i])
                if sucess:
                    rh_test_mesh.Append(rh_b_mesh_faces[j])
            rh_meshes.append(rh_test_mesh)
            df_b_mesh_faces = [df_cvt_bindings.cvt_rhmesh_2_dfmesh(rh_b_mesh_face) for rh_b_mesh_face in rh_b_mesh_faces]

            # different association depending on the type of beam
            df_new_asssociated_cluster_faces = dfb_segmentation.DFSegmentation.associate_clusters(
                is_roundwood=df_b.is_roundwood,
                discriminate_points=True,
                reference_mesh=df_b_mesh_faces,
                unassociated_clusters=df_clouds,
                angle_threshold=i_angle_threshold,
                association_threshold=i_association_threshold,
                maximum_face_segment_distance=i_maximum_face_segment_distance
            )
            df_asssociated_cluster_faces_per_beam.append(df_new_asssociated_cluster_faces)

        for i, df_b in enumerate(df_beams):
            o_face_clusters.append([])
            rh_b_mesh_faces = [df_b_f.to_mesh() for df_b_f in df_b.side_faces]
            for j in range(len(rh_b_mesh_faces)):
                rh_b_mesh_faces[j].Transform(o_transforms[i])
            df_b_mesh_faces = [df_cvt_bindings.cvt_rhmesh_2_dfmesh(rh_b_mesh_face) for rh_b_mesh_face in rh_b_mesh_faces]

            dfb_segmentation.DFSegmentation.clean_unassociated_clusters(
                is_roundwood=df_b.is_roundwood,
                discriminate_points=True,
                unassociated_clusters=df_clouds,
                associated_clusters=[df_asssociated_cluster_faces_per_beam[i]],
                reference_mesh=[df_b_mesh_faces],
                angle_threshold=i_angle_threshold,
                association_threshold=i_association_threshold,
                maximum_face_segment_distance=i_maximum_face_segment_distance
            )

            o_face_clusters[-1] = [df_cvt_bindings.cvt_dfcloud_2_rhcloud(cluster) for cluster in df_asssociated_cluster_faces_per_beam[i]]

            df_asssociated_cluster = dfb_geometry.DFPointCloud()
            for df_associated_face in df_asssociated_cluster_faces_per_beam[i]:
                df_asssociated_cluster.add_points(df_associated_face)

            df_clusters.append(df_asssociated_cluster)

        o_beam_clouds = [df_cvt_bindings.cvt_dfcloud_2_rhcloud(cluster) for cluster in df_clusters]

        for i, o_beam_cloud in enumerate(o_beam_clouds):
            if not o_beam_cloud.IsValid:
                o_beam_clouds[i] = None
                ghenv.Component.AddRuntimeMessage(RML.Warning, "Some beams could not be segmented and were replaced by 'None'")  # noqa: F821

        o_face_clouds = th.list_to_tree(o_face_clusters)

        return [o_beam_clouds, o_face_clouds]
