import Rhino as rc
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import scriptcontext as sc

import log
import util
import acim
import visual_debug as vd

import random

def parse_data_from_brep(ACIM,
                         p_GUID,
                         cut_b,
                         bbox_b):
    """
        Parse data from a brep defining a cut
        :param ACIM: the ACIM object to export xml
        :param p_GUID: the guid of the timber
        :param box_b: the brep defining the cut
        :param bbox_b: the brep of the bounding box
    """
    log.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    log.info("Parsing cut data..")
    bbox_faces_b = util.explode_brep(bbox_b)
    cut_faces_b = util.explode_brep(cut_b)
    log.info("Cut faces: " + str(len(cut_faces_b)))

    acim_faces = []
    acim_edges = []
    # template dicts for faces and lines
    acim_face_dict = {"face_id" : "1",                        # the id of the face
                      "exposed" : "True",                     # if the face is exposed
                      "edges" : "1 2 3",                      # the ids of the lines
                      "corners" : ["0 0 0", "1 1 1", "2 2 2"] # the coordinates of the corners
                      }
    acim_edge_dict = {"line_id" : "1",                        # the id of the line
                      "start" : "0 0 0",                      # the start point of the line
                      "end" : "1 1 1",                        # the end point of the line
                      "exposed" : "true",                     # if the line is exposed
                      }

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    log.info("Detecting cut centroid..")
    cut_centroid = cut_b.GetBoundingBox(True).Center
    cut_centroid_str = str(cut_centroid.X) + " " + str(cut_centroid.Y) + " " + str(cut_centroid.Z)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    log.info("Parsing lines..")
    clr_edge = (0,0,0)
    face_edges = cut_b.Edges
    is_on_face = False
    TEMP_line_ids = []
    TEMP_line_midpoints = []
    for i, face_edge in enumerate(face_edges):
        acim_edge_dict["line_id"] = str(i)
        acim_edge_dict["start"] = str(face_edge.PointAtStart.X) + " " + str(face_edge.PointAtStart.Y) + " " + str(face_edge.PointAtStart.Z)
        acim_edge_dict["end"] = str(face_edge.PointAtEnd.X) + " " + str(face_edge.PointAtEnd.Y) + " " + str(face_edge.PointAtEnd.Z)

        face_edge_center = face_edge.PointAtNormalizedLength(0.5)
        if bbox_b.IsPointInside(face_edge_center, sc.doc.ModelAbsoluteTolerance, True):
            is_on_face = False
            clr_edge = (0,255,0)
        else:
            is_on_face = True
            clr_edge = (255,0,0)
        acim_edge_dict["exposed"] = str(is_on_face)

        acim_edges.append(acim_edge_dict.copy())

        vd.addPtName(face_edge.PointAtStart, str(i), clr_edge)
        vd.addLine(rg.Line(face_edge.PointAtStart, face_edge.PointAtEnd), clr_edge)

        TEMP_line_ids.append(i)
        TEMP_line_midpoints.append(face_edge_center)
    
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    log.info("Parsing faces..")
    clr_face = (0,0,0)
    for i, face in enumerate(cut_faces_b):
        edges_candidate_ids = []
        acim_face_dict["face_id"] = str(i)

        face_edges = face.Edges
        is_on_face = False

        # corners
        corners = util.compute_ordered_vertices(face)
        corners_str = []
        for corner in corners:
            corners_str.append(str(corner.X) + " " + str(corner.Y) + " " + str(corner.Z))
        acim_face_dict["corners"] = corners_str

        # edges indices
        for i, face_edge in enumerate(face_edges):
            face_edge_center = face_edge.PointAtNormalizedLength(0.5)
            idx = util.detect_idx_pt_in_list(face_edge_center, TEMP_line_midpoints)
            if idx != -1:
                edges_candidate_ids.append(TEMP_line_ids[idx])
            vertex = face_edge.PointAtStart
        acim_face_dict["edges"] = " ".join(str(x) for x in edges_candidate_ids)

        # face exposed value
        polyline_corners = corners
        polyline_corners.append(corners[0])
        polyline = rg.Polyline(corners)
        # vd.addPolyline(polyline, (0,0,0))
        face_center = polyline.CenterPoint()
        # log.info("Face center: " + str(face_center))
        # vd.addBrep(bbox_b, (0,0,0))
        if bbox_b.IsPointInside(face_center, sc.doc.ModelAbsoluteTolerance, True):
            is_on_face = False
            clr_face = (0,255,0)
        else:
            is_on_face = True
            clr_face = (255,0,0)
        vd.addPtName(face_center, acim_face_dict["edges"], clr_face)
        acim_face_dict["exposed"] = str(is_on_face)

        acim_faces.append(acim_face_dict.copy())

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    log.info("Dumping cut in acim..")
    ACIM.add_cut(
        p_GUID,
        cut_centroid_str,
        acim_edges,
        acim_faces
    )
