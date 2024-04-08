import Rhino as rc
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import scriptcontext as sc
import random

import log
import acim
import visual_debug as vd
import util


def _get_radius_from_curved_brep_faces(cylinder_faces_b, start_pt, end_pt):
    for face in cylinder_faces_b:
        if not face.Faces[0].IsPlanar():
            face_curves = face.DuplicateEdgeCurves(True)
            face_crv = face_curves[0]
            pt_base = face_crv.PointAtStart
            axis_ln = rg.Line(start_pt, end_pt)
            radius = axis_ln.DistanceTo(pt_base, False)
            radius = round(radius, 3)
            log.info("radius: " + str(radius))
    return round(radius, 3)

def _get_single_face_brep_center(brep):
    bbox = brep.GetBoundingBox(True)
    bbox_b = bbox.ToBrep()
    center_point = bbox_b.GetBoundingBox(True).Center
    return center_point

def parse_data_from_brep(ACIM,
                         p_GUID,
                         cylinder_b,
                         bbox_b):
    """
        Parse data from a brep defining a hole
        :param ACIM: the ACIM object to export xml
        :param p_GUID: the guid of the timber
        :param cylinder_b: the brep defining the hole
        :param bbox_b: the brep of the bounding box
    """
    log.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    bbox_faces_b = util.explode_brep(bbox_b)
    cylinder_faces_b = util.explode_brep(cylinder_b)
    log.info("cylinder faces: " + str(len(cylinder_faces_b)))
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # get the centers of the cylinder's bases and if they are exposed
    acim_centers = {}
    for face in cylinder_faces_b:
        if face.Faces[0].IsPlanar():
            continue
        face_curves = face.DuplicateEdgeCurves(True)
        for face_crv in face_curves:
            face_crv_center = util.get_crv_circle_center(face_crv)
            is_on_face = False
            if bbox_b.IsPointInside(face_crv_center, sc.doc.ModelAbsoluteTolerance, True):
                if util.is_pt_unique_in_dict(face_crv_center, acim_centers):
                    acim_centers[face_crv_center] = is_on_face
                    vd.addPt(face_crv_center, (0,255,0))
                    continue
            if rs.IsPointOnSurface(face, face_crv_center):
                is_on_face = True
            if util.is_pt_unique_in_dict(face_crv_center, acim_centers):
                acim_centers[face_crv_center] = is_on_face
                vd.addPt(face_crv_center, (255,0,0))
    log.info("length of acim_centers: " + str(len(acim_centers)))

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # parse simple holes or sub-holes
    centers_len = len(acim_centers)
    if centers_len == 0:
        log.error("No center found for the hole. Exiting...")
        return
    if centers_len == 1:
        log.info("Single center found for the hole. Exiting...")
        return
    if centers_len == 2:
        log.info("Simple 2-points hole detected")
        start_pt = rg.Point3d(0,0,0)
        end_pt = rg.Point3d(0,0,0)
        is_start_pt_accessible = False
        is_end_pt_accessible = False
        if acim_centers.values()[0]:
            start_pt = acim_centers.keys()[0]
            end_pt = acim_centers.keys()[1]
            is_start_pt_accessible = acim_centers.values()[0]
            is_end_pt_accessible = acim_centers.values()[1]
        else:
            start_pt = acim_centers.keys()[1]
            end_pt = acim_centers.keys()[0]
            is_start_pt_accessible = acim_centers.values()[1]
            is_end_pt_accessible = acim_centers.values()[0]

        radius = _get_radius_from_curved_brep_faces(cylinder_faces_b, start_pt, end_pt)
        log.info("radius: " + str(radius))
        vd.addLine(rg.Line(start_pt, end_pt), (255,165,0))
        vd.addDotPt(ptA=start_pt, ptB=end_pt, clr=(0,255,0), txt=str(ACIM.peek_current_hole_id(p_GUID)))
        
        for face in cylinder_faces_b:
            if not face.Faces[0].IsPlanar():
                face_curves = face.DuplicateEdgeCurves(True)
                vd.addCurve(face_curves[0], (255,0,255))
                vd.addCurve(face_curves[1], (255,0,255))

        ACIM.add_hole(p_GUID,
                    start_pt,
                    end_pt,
                    is_start_pt_accessible,
                    is_end_pt_accessible,
                    radius)
    if centers_len > 2:
        log.info("Complex hole detected")
        holes = []
        
        # get longest line
        dists = []
        extreme_pts = []
        for i in range(0, centers_len):
            for j in range(i+1, centers_len):
                pt1 = acim_centers.keys()[i]
                pt2 = acim_centers.keys()[j]
                dist = pt1.DistanceTo(pt2)
                dists.append(dist)
                if dist >= max(dists) or len(dists) == 0:
                    extreme_pts = [i, j]

        extreme_pts = [acim_centers.keys()[extreme_pts[0]],
                       acim_centers.keys()[extreme_pts[1]]]
        longest_ln = rg.Line(extreme_pts[0], extreme_pts[1])
        longest_crv = longest_ln.ToNurbsCurve()

        centers_lst_reorder = list(acim_centers.keys())
        centers_lst_reorder.sort(key=lambda x: extreme_pts[0].DistanceTo(x))

        #create segments
        hole_axis_ln = []
        for i in range(0, centers_len-1):
            pt1 = centers_lst_reorder[i]
            pt2 = centers_lst_reorder[i+1]
            ln = rg.Line(pt1, pt2)
            hole_axis_ln.append(ln)
        
        # detect neighbours
        neighbor_lst = []
        for i in range(0, len(hole_axis_ln)):
            for j in range(0, len(hole_axis_ln)):
                if i == j:
                    continue
                if hole_axis_ln[i].DistanceTo(hole_axis_ln[j].From, False) < 0.01:
                    neighbor_lst.append([i, j])
                    break
                if hole_axis_ln[i].DistanceTo(hole_axis_ln[j].To, False) < 0.01:
                    neighbor_lst.append([i, j])
                    break
        log.info("neighbor pattern for current hole set: " + str(neighbor_lst))
        next_hole_ids = []
        current_hole_id = ACIM.peek_current_hole_id(p_GUID)
        for i in range(1, len(neighbor_lst)+1):
            next_hole_ids.append(current_hole_id)
            current_hole_id += 1
        log.info("next hole ids: " + str(next_hole_ids))
        neighbor_acim_str = []
        for i in range(0, len(neighbor_lst)):
            temp_str = ""
            for j in range(1, len(neighbor_lst[i])):
                temp_str += str(next_hole_ids[neighbor_lst[i][j]]) + " "
            temp_str = temp_str[:-1]
            neighbor_acim_str.append(temp_str)
        log.info("neighbor acim str: " + str(neighbor_acim_str))

        for i, axis_ln in enumerate(hole_axis_ln):
            vd.addLine(axis_ln, (255,165,0))
            vd.addDotLn(ln=axis_ln, clr=(30,255,230), txt=str(ACIM.peek_current_hole_id(p_GUID)))

            start_pt = rg.Point3d(0,0,0)
            end_pt = rg.Point3d(0,0,0)
            is_start_pt_accessible = False
            is_end_pt_accessible = False
            pt_1 = axis_ln.PointAt(0)
            pt_2 = axis_ln.PointAt(1)
            if acim_centers[pt_1]:
                start_pt = pt_1
                end_pt = pt_2
                is_start_pt_accessible = acim_centers[pt_1]
                is_end_pt_accessible = acim_centers[pt_2]
            else:
                start_pt = pt_2
                end_pt = pt_1
                is_start_pt_accessible = acim_centers[pt_2]
                is_end_pt_accessible = acim_centers[pt_1]
            
            for face in cylinder_faces_b:
                if not face.Faces[0].IsPlanar():
                    radius = 0
                    face_curves = face.DuplicateEdgeCurves(True)
                    face_center_A = util.get_crv_circle_center(face_curves[0])
                    face_center_B = util.get_crv_circle_center(face_curves[1])

                    vd.addCurve(face_curves[0], (255,0,255))
                    vd.addCurve(face_curves[1], (255,0,255))

                    f_0X = round(face_center_A.X, 3)
                    f_0Y = round(face_center_A.Y, 3)
                    f_0Z = round(face_center_A.Z, 3)

                    f_1X = round(face_center_B.X, 3)
                    f_1Y = round(face_center_B.Y, 3)
                    f_1Z = round(face_center_B.Z, 3)

                    sX = round(start_pt.X, 3)
                    sY = round(start_pt.Y, 3)
                    sZ = round(start_pt.Z, 3)

                    eX = round(end_pt.X, 3)
                    eY = round(end_pt.Y, 3)
                    eZ = round(end_pt.Z, 3)

                    if (f_0X == sX and f_0Y == sY and f_0Z == sZ) or (f_0X == eX and f_0Y == eY and f_0Z == eZ):  # = start
                        if (f_1X == sX and f_1Y == sY and f_1Z == sZ) or (f_1X == eX and f_1Y == eY and f_1Z == eZ):  # = end
                            ellipse_pt = face_curves[0].PointAtStart
                            radius = axis_ln.DistanceTo(ellipse_pt, False)
                            radius = round(radius, 3)
                            log.info("radius: " + str(radius))
                            break

            ACIM.add_hole(p_GUID,
                        start_pt,
                        end_pt,
                        is_start_pt_accessible,
                        is_end_pt_accessible,
                        radius,
                        neighbours=neighbor_acim_str[i])







        

