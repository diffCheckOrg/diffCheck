import Rhino
import diffCheck.df_cvt_bindings as df_cvt
import diffCheck.df_geometries as df_geo
import diffCheck.diffcheck_bindings as df_bindings

def main(model, voxel_size, normal_threshold, min_cluster_size):
    a = []
    df_scan = df_cvt.cvt_rhcloud_2_dfcloud(scan)
    res = df_bindings.dfb_segmentation.DFSegmentation.segmentation_point_cloud(df_scan, voxel_size, normal_threshold, min_cluster_size)
    print(len(res))
    for pc in res:
        a.append(pc)
    
    

    for brep in model:
        brep_faces = brep.Faces
        center_points = []
        for i in range(brep_faces.Count):
            brep_face = brep_faces.ExtractFace(i)
            face_vertices = brep_face.Vertices
            center_point = Rhino.Geometry.Point3d(0, 0, 0)
            for j in range(face_vertices.Count):
                vertex = face_vertices[j]
                center_point += vertex.Location
            center_point /= face_vertices.Count
            for face in a:
                initial_distance = center_point - face.get_center_point()
                print(initial_distance)
    return a, center_points

if __name__ == "__main__":
    a, center_points = main(model, voxel_size, normal_threshold, min_cluster_size)