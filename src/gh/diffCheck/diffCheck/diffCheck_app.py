#! python3
import Rhino
import Rhino.Geometry as rg
import scriptcontext as sc

import os
import typing

from df_geometries import DFVertex, DFFace, DFBeam, DFAssembly  # diffCheck.
import df_transformations  # diffCheck.
import df_joint_detector  # diffCheck.
import df_util  # diffCheck.


if __name__ == "__main__":

    print("Running diffCheck...")
    x_form = df_transformations.pln_2_pln_world_transform(i_brep)

    # reverse the transformation
    x_form_back = df_transformations.get_inverse_transformation(x_form)

    # i_brep.Transform(x_form_back)
    # o_brep = i_brep
    

    # compute the bounding box and inflate to include butt joints typo
    bbox = i_brep.GetBoundingBox(True)
    diagonal = bbox.Diagonal
    scaling_factor = diagonal.Length / 10
    bbox.Inflate(
        scaling_factor, 0, 0
    )
    bbox_b = bbox.ToBrep()

    print("Bounding box computed...")
    # boolean difference between the bounding box and the brep transformed
    brep_result = Rhino.Geometry.Brep.CreateBooleanDifference(bbox_b, i_brep, sc.doc.ModelAbsoluteTolerance)
    if brep_result is None or len(brep_result) == 0:
        print("No breps found after boolean difference. Exiting...")
        # return

    ##################################################################
    ##################################################################
    # distinguish holes and cuts
    holes_b, cuts_b = df_joint_detector.distinguish_holes_cuts(brep_result)

    # retransform back everything
    for b in holes_b:
        b.Transform(x_form_back)
    for b in cuts_b:
        b.Transform(x_form_back)
    i_brep.Transform(x_form_back)

    # parse into DFFaces with detection of
    #  - wether it is a joint (bool)
    #  - if it is a hole, which one is (id)

    df_faces = []
    all_faces_centroids : typing.List[rg.Point3d] = []
    cuts_faces_centroids : typing.Dict[int, typing.List[rg.Point3d]] = {}
    detected_facesjoint_centroids : typing.List[rg.Point3d] = []
    side_faces_centroids : typing.List[rg.Point3d] = []

    # get all the medians of the faces of cuts_b
    for idx, b in enumerate(cuts_b):
        temp_face_centroids = []
        for f in b.Faces:
            centroid = DFFace.compute_mass_center(f)
            temp_face_centroids.append(centroid)
        cuts_faces_centroids[idx] = temp_face_centroids

    print(f"Detected faces: {list(cuts_faces_centroids.values()).__len__()}")
    tol = sc.doc.ModelAbsoluteTolerance

    breps = [i_brep]
    for b in breps:
        for f in b.Faces:
            centroid_2test = DFFace.compute_mass_center(f)
            all_faces_centroids.append(centroid_2test)
            
            for idx, centroids in cuts_faces_centroids.items():
                for centroid in centroids:
                    if centroid_2test.DistanceTo(centroid) < tol:
                        df_vertices = []
                        face_loop = f.OuterLoop
                        face_loop_trims = face_loop.Trims
                        for face_loop_trim in face_loop_trims:
                            df_vertices.append(DFVertex.from_rg_point3d(face_loop_trim.PointAtStart))
                        df_faces.append(DFFace(df_vertices, idx))
                        detected_facesjoint_centroids.append(centroid_2test)
                        break
            else:
                df_vertices = []
                face_loop = f.OuterLoop
                face_loop_trims = face_loop.Trims
                for face_loop_trim in face_loop_trims:
                    df_vertices.append(DFVertex.from_rg_point3d(face_loop_trim.PointAtStart))
                df_faces.append(DFFace(df_vertices))
                side_faces_centroids.append(centroid_2test)

    o_brep = cuts_b

    o_centroids1 = side_faces_centroids
    o_centroids2 = detected_facesjoint_centroids

    # beams
    beam = DFBeam("Beam1", df_faces)
    ##################################################################

    # """
    # Main function to test the package
    # :param i_breps: list of breps
    # :param i_export_dir: directory to export the xml
    # :param i_dump: whether to dump the xml
    # """
    # # beams
    # beams : typing.List[DFBeam] = []
    # for brep in i_breps:
    #     beam = DFBeam.from_brep(brep)
    #     beams.append(beam)

    # # assembly
    # assembly1 = DFAssembly(beams, "Assembly1")
    # print(assembly1.beams)
    # print(assembly1)

    # # dump the xml
    # xml : str = assembly1.to_xml()
    # if i_dump:
    #     assembly1.dump(xml, i_export_dir)
    # o_xml = xml