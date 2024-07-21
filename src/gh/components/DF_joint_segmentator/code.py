import Rhino
import diffCheck
from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings as df_cvt
import diffCheck.df_util

def main(pointCloud, breps):
    df_scan = df_cvt.cvt_rhcloud_2_dfcloud(pointCloud)
    meshes = []
    for i in range(breps.BranchCount):
        brep_faces = breps.Branch(i)
        mesh_faces = []
        for brep_face in brep_faces:
            mesh_face = Rhino.Geometry.Mesh.CreateFromBrep(brep_face)[0]
            mesh_face.Faces.ConvertQuadsToTriangles()
            mesh_faces.append(df_cvt.cvt_rhmesh_2_dfmesh(mesh_face))
        meshes.append(mesh_faces)
    associated_segments = []

    # normal segmentation
    segments = diffcheck_bindings.dfb_segmentation.DFSegmentation.segment_by_normal(df_scan, 2, 50, True, 20, 10, False)

    # for visualisation purposes
    rh_segments = []
    for segment in segments:
        rh_segments.append(df_cvt.cvt_dfcloud_2_rhcloud(segment))

    association_results = []
    # associate clusters to pieces
    for piece in meshes:
        associated_segments = diffcheck_bindings.dfb_segmentation.DFSegmentation.associate_clusters(piece, segments)
        diffcheck_bindings.dfb_segmentation.DFSegmentation.clean_unassociated_clusters(segments, associated_segments, piece)
        association_results.append(associated_segments)
    
    return association_results

if __name__ == "__main__":
    a = main(pointCloud, breps)