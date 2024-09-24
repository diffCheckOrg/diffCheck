import Rhino
import Rhino.Geometry as rg
import scriptcontext as sc

import typing


def explode_brep(brep) -> typing.List[Rhino.Geometry.Brep]:
    """ Explode a brep into its faces """
    exploded_objects = []
    if brep.IsSolid:
        for face in brep.Faces:
            face_brep = face.DuplicateFace(False)
            if face_brep:
                exploded_objects.append(face_brep)
    else:
        for face in brep.Faces:
            face_brep = face.DuplicateFace(False)
            if face_brep:
                exploded_objects.append(face_brep)
    return exploded_objects


def get_crv_circle_center(crv) -> rg.Point3d:
    """ Get the center of a circle """
    bbox = crv.GetBoundingBox(True)
    bbox_b = bbox.ToBrep()
    center_point = bbox_b.GetBoundingBox(True).Center
    return center_point


def is_pt_unique_in_dict(pt, pt_dict) -> bool:
    """
        Detect if the point exists in the dictionary, and if so, return the index

        :param pt: the point to check
        :param pt_dict: the dictionary to check
        :return: True if the point is unique, False otherwise
    """
    is_unique = True
    for pt_dict in pt_dict.keys():
        X_a = round(pt.X, 3)
        Y_a = round(pt.Y, 3)
        Z_a = round(pt.Z, 3)

        X_b = round(pt_dict.X, 3)
        Y_b = round(pt_dict.Y, 3)
        Z_b = round(pt_dict.Z, 3)

        if X_a == X_b and Y_a == Y_b and Z_a == Z_b:
            is_unique = False
            break
    return is_unique


def is_pt_unique_in_list(pt, list) -> bool:
    """
        Detect if the point exists in the list, and if so, return the index

        :param pt: the point to check
        :param list: the list to check
        :return: True if the point is unique, False otherwise
    """
    is_unique = True
    for pt_list in list:
        X_a = round(pt.X, 3)
        Y_a = round(pt.Y, 3)
        Z_a = round(pt.Z, 3)

        X_b = round(pt_list.X, 3)
        Y_b = round(pt_list.Y, 3)
        Z_b = round(pt_list.Z, 3)

        if X_a == X_b and Y_a == Y_b and Z_a == Z_b:
            is_unique = False
            break
    return is_unique


def detect_idx_pt_in_list(pt, list) -> int:
    """
        Detect the index of a point in a list

        :param pt: the point to check
        :param list: the list to check
        :return: the index of the point in the list
    """
    idx = -1
    for pt_list in list:
        idx += 1
        X_a = round(pt.X, 3)
        Y_a = round(pt.Y, 3)
        Z_a = round(pt.Z, 3)

        X_b = round(pt_list.X, 3)
        Y_b = round(pt_list.Y, 3)
        Z_b = round(pt_list.Z, 3)

        if X_a == X_b and Y_a == Y_b and Z_a == Z_b:
            return idx
    return idx


def compute_ordered_vertices(brep_face) -> typing.List[Rhino.Geometry.Point3d]:
    """ Retrieve the ordered vertices of a brep face """
    sorted_vertices = []

    edges = brep_face.DuplicateEdgeCurves()
    edges = list(set(edges))

    edges_sorted: list[Rhino.Geometry.Curve] = []
    while len(edges) > 0:
        if len(edges_sorted) == 0:
            edges_sorted.append(edges[0])
            edges.pop(0)
        else:
            for edge in edges:
                if edges_sorted[-1].PointAtStart == edge.PointAtStart:
                    edges_sorted.append(edge)
                    edges.pop(edges.index(edge))
                    break
                elif edges_sorted[-1].PointAtStart == edge.PointAtEnd:
                    edges_sorted.append(edge)
                    edges.pop(edges.index(edge))
                    break
                elif edges_sorted[-1].PointAtEnd == edge.PointAtStart:
                    edges_sorted.append(edge)
                    edges.pop(edges.index(edge))
                    break
                elif edges_sorted[-1].PointAtEnd == edge.PointAtEnd:
                    edges_sorted.append(edge)
                    edges.pop(edges.index(edge))
                    break

    for edge in edges_sorted:
        sorted_vertices.append(edge.PointAtStart)

    return sorted_vertices

def get_doc_2_meters_unitf():
    """
        Retrieve the document unit system and get the multiplier factor to
        be multiplied to all the component's inputs for df functions since they
        are all based in meters.

        :return: the multiplier factor to be multiplied to the inputs to convert them to meters
    """
    RhinoDoc = sc.doc
    if RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Meters:
        unit_scale = 1
    elif RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Centimeters:
        unit_scale = 0.01
    elif RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Millimeters:
        unit_scale = 0.001
    elif RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Inches:
        unit_scale = 0.0254
    elif RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Feet:
        unit_scale = 0.3048
    elif RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Yards:
        unit_scale = 0.9144
    return unit_scale

def merge_shared_indexes(original_dict):
    """
    Merge the shared indexes of a dictionary

    Assume we have a dictionary with lists of indexes as values.
    We want to merge the lists that share some indexes, in order to have a dictionary with, for each key, indexes that are not present under other keys.

    :param original_dict: the dictionary to merge
    :return: the merged dictionary
    """
    merged_dict = {}
    index_to_key = {}

    for key, (face, indexes) in original_dict.items():
        merged_indexes = set(indexes)
        keys_to_merge = set()

        for index in indexes:
            if index in index_to_key:
                keys_to_merge.add(index_to_key[index])

        for merge_key in keys_to_merge:
            merged_indexes.update(merged_dict[merge_key][1])
            # del merged_dict[merge_key]

        for index in merged_indexes:
            index_to_key[index] = key

        merged_dict[key] =  (face, list(merged_indexes))

    keys_with_duplicates = {}

    for key in merged_dict.keys():
        for other_key, (face, indexes) in merged_dict.items():
            if key in indexes:
                if key not in keys_with_duplicates:
                    keys_with_duplicates[key] = []
                keys_with_duplicates[key].append(other_key)

    return merged_dict
