import Rhino
import Rhino.Geometry as rg
import scriptcontext as sc

import numpy as np


def get_inverse_transformation(
    x_form: Rhino.Geometry.Transform,
) -> Rhino.Geometry.Transform:
    """
        Get the inverse of a transformation
        
        :param x_form: the transformation to get the inverse from
        :return: the inverse transformation
    """
    transformation_matrix = np.array(
        [
            [x_form.M00, x_form.M01, x_form.M02, x_form.M03],
            [x_form.M10, x_form.M11, x_form.M12, x_form.M13],
            [x_form.M20, x_form.M21, x_form.M22, x_form.M23],
            [x_form.M30, x_form.M31, x_form.M32, x_form.M33],
        ]
    )
    inverse_transformation_matrix = np.linalg.inv(transformation_matrix)

    x_form_back = Rhino.Geometry.Transform()
    for i in range(4):
        for j in range(4):
            x_form_back[i, j] = inverse_transformation_matrix[i, j]

    return x_form_back


def pln_2_pln_world_transform(brep: Rhino.Geometry.Brep) -> Rhino.Geometry.Transform:
    """
        Transform a brep (beam) to the world plane
        
        :param brep: the brep to transform
        :return: the transformation
    """

    def _get_lowest_brep_vertex(brep) -> Rhino.Geometry.Point3d:
        """
            Get the the vertex with the lowest y,x and z values
            
            :param brep: the brep to get the lowest vertex from
            :return: the lowest vertex
        """
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
        return Rhino.Geometry.Point3d(lowest_x, lowest_y, lowest_z)

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
        log.error("Could not find plane for longest edge. Exiting...")
        return
    plane_src = biggest_face.TryGetPlane()[1]
    plane_tgt = Rhino.Geometry.Plane.WorldXY

    # plane to plane transformation
    x_form_pln2pln = Rhino.Geometry.Transform.PlaneToPlane(plane_src, plane_tgt)
    brep.Transform(x_form_pln2pln)

    # adjust to x,y,z positive
    lowest_vertex = _get_lowest_brep_vertex(brep)
    x_form_transl_A = Rhino.Geometry.Transform.Translation(rg.Vector3d(-lowest_vertex))
    brep.Transform(x_form_transl_A)

    # aabb
    bbox = brep.GetBoundingBox(True)
    bbox_corners = bbox.GetCorners()
    y_val_sum = 0
    x_val_sum = 0
    for corner in bbox_corners:
        y_val_sum += corner.Y
        x_val_sum += corner.X

    # check if a 90 deg rotation is needed (for the joint detector)
    x_form_transl_B = None
    x_form_rot90z = None
    if x_val_sum > y_val_sum:
        # AABB is alligned to x axis. No rotation needed
        pass
    else:
        # AABB is not alligned to y axis. A 90 deg rotation is needed.
        x_form_rot90z = Rhino.Geometry.Transform.Rotation(
            math.radians(90), rg.Vector3d.ZAxis, rg.Point3d.Origin
        )
        brep.Transform(x_form_rot90z)
        lowest_vertex = _get_lowest_brep_vertex(brep)

        x_form_transl_B = Rhino.Geometry.Transform.Translation(
            rg.Vector3d(-lowest_vertex)
        )
        brep.Transform(x_form_transl_B)

    # resume the transformations in one
    x_form = Rhino.Geometry.Transform.Identity
    if x_form_transl_B:
        Rhino.Geometry.Transform.TryGetInverse(x_form_transl_B)
        Rhino.Geometry.Transform.TryGetInverse(x_form_rot90z)
        x_form = x_form_transl_B * x_form_rot90z
    x_form = x_form * x_form_transl_A * x_form_pln2pln

    return x_form
