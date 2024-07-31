#! python3

import Rhino

import diffCheck
from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings as df_cvt
import diffCheck.df_util

from ghpythonlib.componentbase import executingcomponent as component

ABSTOL = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

class DFJointSegmentator(component):
    def RunScript(self, 
                  i_clusters: Rhino.Geometry.PointCloud, 
                  i_joints: Rhino.Geometry.Mesh, 
                  i_joint_ids: int,
                  i_angle_threshold: float,
                  i_distance_threshold: float):
        """
        Amongst clusters, associates the clusters to the individual joints, 
        creates a reference point cloud for each joint, 
        and returns the joint segments, the reference point clouds, and the ICP transformations from the first to the second.

        :param i_clusters: The clusters to be associated to the joints.
        :param i_joints: The joints to which the clusters will be associated. These are meshes.
        :param i_joint_ids: The joint ids of the joints.
        :param i_angle_threshold: The angle threshold for the association of the clusters to the joints.
        :param i_distance_threshold: The distance threshold for the association of the clusters to the joints.
        """
        if i_angle_threshold is None : i_angle_threshold = 0.1
        if i_distance_threshold is None : i_distance_threshold = 0.1

        if len(i_joints) != len(i_joint_ids):
            raise ValueError("The number of joints and joint ids must be the same.")
        
        if len(i_clusters) == 0:
            raise ValueError("No clusters given.")

        if not isinstance(i_clusters[0], Rhino.Geometry.PointCloud):
            raise ValueError("The input clusters must be PointClouds.")
        
        if not isinstance(i_joints[0], Rhino.Geometry.Mesh):
            raise ValueError("The input joints must be convertible to Meshes.")
            

        # prepping the reference meshes
        n_joints = max(i_joint_ids) + 1
        joints = [ [] for i in range(n_joints) ]
        for face, id in zip(i_joints, i_joint_ids):
            face.Subdivide()
            face.Faces.ConvertQuadsToTriangles()
            joints[id].append(df_cvt.cvt_rhmesh_2_dfmesh(face))

        joint_clouds = []
        registrations = []
        joint_segments = []
        df_clouds = [df_cvt.cvt_rhcloud_2_dfcloud(cluster) for cluster in i_clusters]

        # for each joint, find the corresponding clusters and merge them, generate a reference point cloud, and register the merged clusters to the reference point cloud
        for joint in joints:

            # create the reference point cloud
            joint_cloud = diffcheck_bindings.dfb_geometry.DFPointCloud()

            for face in joint:
                face_cloud = face.sample_points_uniformly(1000)
                joint_cloud.add_points(face_cloud)

            joint_clouds.append(df_cvt.cvt_dfcloud_2_rhcloud(joint_cloud))

            # find the corresponding clusters and merge them
            segment = diffcheck_bindings.dfb_segmentation.DFSegmentation.associate_clusters(joint, df_clouds, i_angle_threshold, i_distance_threshold)
            diffcheck_bindings.dfb_segmentation.DFSegmentation.clean_unassociated_clusters(df_clouds, [segment], [joint], i_angle_threshold ,i_distance_threshold)

            # register the merged clusters to the reference point cloud
            registration = diffcheck_bindings.dfb_registrations.DFRefinedRegistration.O3DICP(segment, joint_cloud)
            res = registration.transformation_matrix

            registrations.append(df_cvt.cvt_ndarray_2_rh_transform(res))
            joint_segments.append(df_cvt.cvt_dfcloud_2_rhcloud(segment))

        return joint_segments, registrations, joint_clouds

# if __name__ == "__main__":
#     o_joint_segments, o_reference_point_clouds, o_transforms = main(i_clusters, i_joints, i_joint_ids)

#     for i in range(len(o_joint_segments)):
#         o_joint_segments[i].Transform(o_transforms[i])
