#! python3

import Rhino
import diffCheck
from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings as df_cvt
import diffCheck.df_util
import scriptcontext as sc

ABSTOL = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

def main(i_clusters, i_joints, i_joint_ids):

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
            face_cloud.estimate_normals(knn=30)
            joint_cloud.add_points(face_cloud)

        joint_clouds.append(df_cvt.cvt_dfcloud_2_rhcloud(joint_cloud))

        # find the corresponding clusters and merge them
        segment = diffcheck_bindings.dfb_segmentation.DFSegmentation.associate_clusters(joint, df_clouds )
        diffcheck_bindings.dfb_segmentation.DFSegmentation.clean_unassociated_clusters(df_clouds, [segment], [joint], 0.1, 0.02)

        # register the merged clusters to the reference point cloud
        registration = diffcheck_bindings.dfb_registrations.DFRefinedRegistration.O3DICP(segment, joint_cloud)
        res = registration.transformation_matrix

        registrations.append(df_cvt.cvt_ndarray_2_rh_transform(res))
        joint_segments.append(df_cvt.cvt_dfcloud_2_rhcloud(segment))

    return joint_segments, joint_clouds, registrations

if __name__ == "__main__":
    o_joint_segments, o_reference_point_clouds, o_transforms = main(i_clusters, i_joints, i_joint_ids)

    for i in range(len(o_joint_segments)):
        o_joint_segments[i].Transform(o_transforms[i])
