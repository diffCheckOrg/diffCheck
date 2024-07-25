#! python3

import Rhino
import diffCheck
from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings as df_cvt
import diffCheck.df_util
import scriptcontext as sc

ABSTOL = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

def main(i_clusters, i_faces, i_joint_ids):
    n_joints = max(i_joint_ids) + 1
    joints = [ [] for i in range(n_joints) ]
    for face, id in zip(i_faces, i_joint_ids):
        face.Subdivide()
        face.Faces.ConvertQuadsToTriangles()
        joints[id].append(df_cvt.cvt_rhmesh_2_dfmesh(face))
    joint_clouds = []
    registrastions = []
    joint_segments = []
    df_clouds = [df_cvt.cvt_rhcloud_2_dfcloud(cluster) for cluster in i_clusters]

    for joint in joints:
        joint_cloud = diffcheck_bindings.dfb_geometry.DFPointCloud()
        for face in joint:
            face_cloud = face.sample_points_uniformly(1000)
            face_cloud.estimate_normals(knn=30)
            joint_cloud.add_points(face_cloud)
        joint_clouds.append(df_cvt.cvt_dfcloud_2_rhcloud(joint_cloud))
        segment = diffcheck_bindings.dfb_segmentation.DFSegmentation.associate_clusters(joint, df_clouds )
        diffcheck_bindings.dfb_segmentation.DFSegmentation.clean_unassociated_clusters(df_clouds, [segment], [joint], 0.1, 0.02)
        registration = diffcheck_bindings.dfb_registrations.DFRefinedRegistration.O3DICP(segment, joint_cloud)
        res = registration.transformation_matrix
        registrastions.append(res)
        joint_segments.append(df_cvt.cvt_dfcloud_2_rhcloud(segment))

    return joint_segments, joint_clouds, registrastions

if __name__ == "__main__":
    joint_segments, joint_clouds, registrastions = main(i_clusters, i_faces, i_joint_ids)

    for i in range(len(joint_segments)):
        joint_segments[i].Transform(df_cvt.cvt_ndarray_2_rh_transform(registrastions[i]))
