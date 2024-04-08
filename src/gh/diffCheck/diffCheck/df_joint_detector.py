import rhinoscriptsyntax as rs
import Rhino as rc
import scriptcontext as sc
import Rhino.Geometry as rg
import datetime as dt
import math

import log
import hole
import cut
import util

# import visual_debug as vd

def get_lowest_brep_vertex(brep):
    """ Get the the vertex with the lowest y,x and z values """
    biggest_vertices = brep.Vertices
    lowest_x = 0
    lowest_y = 0
    lowest_z = 0
    for vertex in biggest_vertices:
        if vertex.Location.X < lowest_x:
            lowest_x = vertex.Location.X
        if vertex.Location.Y < lowest_y:
            lowest_y = vertex.Location.Y
        if vertex.Location.Z < lowest_z:
            lowest_z = vertex.Location.Z
    return rc.Geometry.Point3d(lowest_x, lowest_y, lowest_z)

def pln_2_pln_world_transform(brep):
    """ Transform a brep to the world plane """
    print("Computing Oriented Bounding Boxes...")

    # find the longest edge of the brep
    edges = brep.Edges
    longest_edge = None
    longest_edge_length = 0
    for edge in edges:
        if edge.GetLength() > longest_edge_length:
            longest_edge_length = edge.GetLength()
            longest_edge = edge

    # find biggest face
    face_indices = longest_edge.AdjacentFaces()
    faces = [brep.Faces[face_index] for face_index in face_indices]
    biggest_face = None
    biggest_face_area = 0
    for face in faces:
        if rg.AreaMassProperties.Compute(face).Area > biggest_face_area:
            biggest_face_area = rg.AreaMassProperties.Compute(face).Area
            biggest_face = face
    
    # get the plane of the biggest face
    if biggest_face.TryGetPlane()[0] is False:
        print("Could not find plane for longest edge. Exiting...")
        return
    plane_src = biggest_face.TryGetPlane()[1]
    plane_tgt = rc.Geometry.Plane.WorldXY
    print("Found plane for longest edge: " + str(plane_src))

    # plane to plane transformation
    plane_to_world = rc.Geometry.Transform.PlaneToPlane(plane_src, plane_tgt)
    brep.Transform(plane_to_world)

    # adjust to x,y,z positive
    lowest_vertex = get_lowest_brep_vertex(brep)
    lowest_vertex_transform = rc.Geometry.Transform.Translation(rg.Vector3d(-lowest_vertex))
    brep.Transform(lowest_vertex_transform)

    bbox = brep.GetBoundingBox(True)
    bbox_corners = bbox.GetCorners()
    y_val_sum = 0
    x_val_sum = 0
    for corner in bbox_corners:
        y_val_sum += corner.Y
        x_val_sum += corner.X

    if x_val_sum > y_val_sum:
        print("Bounding box is alligned to x axis. No rotation needed.")
    else:
        print("Bounding box is not alligned to y axis. A 90 deg rotation is needed.")
        rot_90_z = rc.Geometry.Transform.Rotation(math.radians(90), rg.Vector3d.ZAxis, rg.Point3d.Origin)
        brep.Transform(rot_90_z)
        lowest_vertex = get_lowest_brep_vertex(brep)

        lowest_vertex_transform = rc.Geometry.Transform.Translation(rg.Vector3d(-lowest_vertex))
        brep.Transform(lowest_vertex_transform)

    # vd.addBrep(brep, clr=(255, 0, 0, 30))

def distinguish_holes_cuts(breps):
    """ 
        Analyse the result breps from the boolean difference operation
        and distinguish between holes and cuts
    """
    is_hole = False
    is_cut = False
    is_mix = False
    holes_b = []
    cuts_b = []
    mix_b = []

    # parse holes, cuts and mix
    for b in breps:
        is_cut = True
        for f in b.Faces:
            f_brep = f.ToBrep()
            f = f_brep.Faces[0]
            if not f.IsPlanar():
                is_cut = False
                is_hole = True
                b_faces = util.explode_brep(b)
                for b_face in b_faces:
                    if b_face.Faces[0].IsPlanar():
                        b_face_edges = b_face.Edges
                        for b_face_edge in b_face_edges:
                            if not b_face_edge.IsClosed:
                                is_mix = True
                                is_hole = False
                                break
                        if is_mix:
                            break
                break

        if is_hole:
            holes_b.append(b)
        elif is_cut: 
            cuts_b.append(b)
        elif is_mix:
            mix_b.append(b)

        is_hole = False
        is_cut = False
        is_mix = False
    
    # deal with mix
    candidate_cuts = []
    candidate_holes = []
    for b in mix_b:
        # -- algorithm draft --
        # (1) explode
        # (2) seperate in tow list flat surfaces (cuts + cylinder's bases) and non flat surfaces (cylinders)
        # (3) cap each object in both lists
        # (4) boolunion every object in both lists
        # (5) check if closed, if it is 
        # ----------------------
        # (1) explode
        faces_b = util.explode_brep(b)

        # (2) seperate in tow list flat surfaces (cuts + cylinder's bases) and non flat surfaces (cylinders)
        flat_faces_b = []
        non_flat_faces_b = []
        for f_b in faces_b:
            if f_b.Faces[0].IsPlanar():
                flat_faces_b.append(f_b)
            else:
                non_flat_faces_b.append(f_b)
  
        # (*) cap the cylinders
        non_flat_faces_b = [f_b.CapPlanarHoles(sc.doc.ModelAbsoluteTolerance) for f_b in non_flat_faces_b]
        
        # (4) boolunion every object in both lists
        flat_faces_b = rc.Geometry.Brep.CreateBooleanUnion(flat_faces_b, sc.doc.ModelAbsoluteTolerance)
        non_flat_faces_b = rc.Geometry.Brep.CreateBooleanUnion(non_flat_faces_b, sc.doc.ModelAbsoluteTolerance)

        # (3) cap candidate cuts
        flat_faces_b = [f_b.CapPlanarHoles(sc.doc.ModelAbsoluteTolerance) for f_b in flat_faces_b]
        # non_flat_faces_b = [f_b.CapPlanarHoles(sc.doc.ModelAbsoluteTolerance) for f_b in non_flat_faces_b]

        # (*) merge all coplanar faces in breps cut candidates
        for f_b in flat_faces_b:
            if f_b is not None:
                f_b.MergeCoplanarFaces(sc.doc.ModelAbsoluteTolerance)

        # (5) check if closed, if it is add to cuts, if not add to holes
        for f_b in flat_faces_b:
            if f_b is not None:
                if f_b.IsSolid:
                    cuts_b.append(f_b)
        for f_b in non_flat_faces_b:
            if f_b is not None:
                if f_b.IsSolid:
                    holes_b.append(f_b)

    return holes_b, cuts_b

def main():

    # vd.set_on()
    # print(vd.__IS_VDEBUG__)

    print(".acim exporter started")
    rh_doc_path = rs.DocumentPath()
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    acim_path = rh_doc_path + timestamp
    print("Creating ACIM file at: " + acim_path)
    ACIM = acim.ACIM(acim_path)

    pieces = rs.GetObjects("Select pieces to be exported", rs.filter.polysurface, preselect=True)
    if not pieces:
        print("No pieces selected. Exiting...")
        return
    print("Selected " + str(len(pieces)) + " pieces.")

    for p_GUID in pieces:
        print("Processing piece: " + str(p_GUID))
        ACIM.add_timber(str(p_GUID))
        ACIM.add_timber_state(str(p_GUID), 0)
        brep = rs.coercebrep(p_GUID)
        
        # transform to world plane
        pln_2_pln_world_transform(brep)

        # compute the bounding box
        bbox = brep.GetBoundingBox(True)
        bbox_b = bbox.ToBrep()
        ACIM.add_bbox(str(p_GUID), bbox.GetCorners())

        # boolean difference between the bounding box and the brep transformed
        brep_result = rc.Geometry.Brep.CreateBooleanDifference(bbox_b, brep, sc.doc.ModelAbsoluteTolerance)
        if brep_result is None or len(brep_result) == 0:
            log.error("No breps found after boolean difference. Exiting...")
            return

        # get holes and cuts breps
        holes_b, cuts_b = distinguish_holes_cuts(brep_result)
        print("Found:\n" \
            + "\t --holes: " +  str(len(holes_b)) + "\n" \
            + "\t --cuts: " + str(len(cuts_b)) + "\n")

        # analyse and loading holes and cuts into .acim
        if holes_b.__len__() != 0:
            for hole_b in holes_b:
                # vd.addBrep(hole_b, clr=(255, 255, 0, 30))
                print("Processing hole: " + str(hole_b))
                hole.parse_data_from_brep(ACIM, str(p_GUID), hole_b, bbox_b)

        if cuts_b.__len__() != 0:
            cut_counter = 1
            for cut_b in cuts_b:
                # vd.addBrep(cut_b, clr=(255, 0, 255, 30))
                print("Processing cut: " + str(cut_b))
                cut.parse_data_from_brep(ACIM, str(p_GUID), cut_b, bbox_b)

                # vd.addSingleDot(cut_b.GetBoundingBox(True).Center, str(cut_counter), (0,0,255))
                cut_counter += 1

        sc.doc.Views.Redraw()
    ACIM.dump_data()

if __name__ == '__main__':
    main()