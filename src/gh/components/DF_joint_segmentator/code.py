#! python3

import Rhino

from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings as df_cvt

from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
from ghpythonlib.componentbase import executingcomponent as component

import typing

ABSTOL = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

class DFJointSegmentator(component):
    def __init__(self):
        super(DFJointSegmentator, self).__init__()
    def RunScript(self, 
                  i_clusters: typing.List[Rhino.Geometry.PointCloud], 
                  i_assembly: diffCheck.df_geometries.DFAssembly,
                  i_angle_threshold: float,
                  i_distance_threshold: float):

        if i_angle_threshold is None : i_angle_threshold = 0.1
        if i_distance_threshold is None : i_distance_threshold = 0.1
        
        if len(i_clusters) == 0:
            raise ValueError("No clusters given.")
        if not isinstance(i_clusters[0], Rhino.Geometry.PointCloud):
            raise ValueError("The input clusters must be PointClouds.")
            
        # get number of joints
        n_joints = i_assembly.total_number_joints

        # prepping the reference meshes
        df_joints = [[] for _ in range(n_joints)]
        for joint in i_assembly.all_joints:
            for face in joint.faces:
                face = face.to_mesh()
                face.Subdivide()
                face.Faces.ConvertQuadsToTriangles()
                df_joints[joint.id].append(df_cvt.cvt_rhmesh_2_dfmesh(face))

        ref_rh_joint_clouds = []
        transforms = []
        rh_joint_segments = []
        df_cloud_clusters = [df_cvt.cvt_rhcloud_2_dfcloud(cluster) for cluster in i_clusters]

        # for each joint, find the corresponding clusters and merge them, generate a reference point cloud, and register the merged clusters to the reference point cloud
        for df_joint in df_joints:
            # create the reference point cloud
            ref_df_joint_cloud = diffcheck_bindings.dfb_geometry.DFPointCloud()

            for face in df_joint:
                ref_face_cloud = face.sample_points_uniformly(1000)
                ref_df_joint_cloud.add_points(ref_face_cloud)

            ref_rh_joint_clouds.append(df_cvt.cvt_dfcloud_2_rhcloud(ref_df_joint_cloud))

            # find the corresponding clusters and merge them
            df_joint_segment = diffcheck_bindings.dfb_segmentation.DFSegmentation.associate_clusters(df_joint, df_cloud_clusters, i_angle_threshold, i_distance_threshold)
            diffcheck_bindings.dfb_segmentation.DFSegmentation.clean_unassociated_clusters(df_cloud_clusters, [df_joint_segment], [df_joint], i_angle_threshold, i_distance_threshold)
            
            # register the merged clusters to the reference point cloud
            registration = diffcheck_bindings.dfb_registrations.DFRefinedRegistration.O3DICP(df_joint_segment, ref_df_joint_cloud)
            res = registration.transformation_matrix
            transforms.append(df_cvt.cvt_ndarray_2_rh_transform(res))
            rh_joint_segments.append(df_cvt.cvt_dfcloud_2_rhcloud(df_joint_segment))
        
        o_joint_segments = []
        o_transforms = []
        o_reference_point_clouds = []
        for  joint_segment, transform, _joint_cloud in zip(rh_joint_segments, transforms, ref_rh_joint_clouds):
            if joint_segment.IsValid:
                o_joint_segments.append(joint_segment)
                o_transforms.append(transform)
                o_reference_point_clouds.append(_joint_cloud)
            else:
                ghenv.Component.AddRuntimeMessage(RML.Warning, "Some joints could not be segmented and were ignored.")

        return o_joint_segments, o_transforms, o_reference_point_clouds