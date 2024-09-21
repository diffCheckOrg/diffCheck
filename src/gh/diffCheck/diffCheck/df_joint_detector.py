import Rhino
import scriptcontext as sc
import Rhino.Geometry as rg

from dataclasses import dataclass

import diffCheck.df_util
import diffCheck.df_transformations

import numpy as np


@dataclass
class JointDetector:
    """
    This class is responsible for detecting joints in a brep
    """
    brep: Rhino.Geometry.Brep

    def __post_init__(self):
        self._faces = []

    def _assign_ids(self, joint_face_ids):
        """ Return the extended joint ids for each face in the brep """
        joint_ids_is_found = [False] * len(joint_face_ids)
        joint_ids = [None] * len(joint_face_ids)
        id_counter = 0

        for idx_1, joint_face_id_1 in enumerate(joint_face_ids):
            if joint_ids_is_found[idx_1]:
                continue

            joint_ids_is_found[idx_1] = True
            joint_ids[idx_1] = id_counter

            for idx_2, joint_face_id_2 in enumerate(joint_face_ids):
                if any(item in joint_face_id_1 for item in joint_face_id_2):
                    joint_ids_is_found[idx_2] = True
                    joint_ids[idx_2] = id_counter

            id_counter += 1

        extended_ids = [None] * self.brep.Faces.Count
        for idx, joint_id in enumerate(joint_ids):
            for joint_face_id in joint_face_ids[idx]:
                extended_ids[joint_face_id] = joint_id

        return extended_ids

    def find_largest_cylinder(self):
        """
            Finds and returns the largest cylinder in the brep

            :return: the largest cylinder if beam detected as a cylinder, None otherwise
        """

        # extract all cylinders from the brep
        candidate_open_cylinders = []
        for face in self.brep.Faces:
            if not face.IsPlanar():
                candidate_open_cylinder = face.ToBrep()
                candidate_open_cylinders.append(candidate_open_cylinder)

        # find largest cylinder
        largest_cylinder = None
        largest_srf = 0
        for candidate_cylinder in candidate_open_cylinders:
            area = candidate_cylinder.GetArea()
            if area > largest_srf and candidate_cylinder.CapPlanarHoles(sc.doc.ModelAbsoluteTolerance):
                largest_srf = area
                largest_cylinder = candidate_cylinder.CapPlanarHoles(sc.doc.ModelAbsoluteTolerance)
        print(largest_srf)

        # Check if the cylinder exists
        if largest_cylinder is None:
            print("No cylinder found")
            return None

        return largest_cylinder


    def run(self, is_cylinder_beam):
        """
            Run the joint detector. We use a dictionary to store the faces of the cuts based wethear they are cuts or holes.
            - for cuts: If it is a cut we return the face, and the id of the joint the faces belongs to.
            - for sides: If it is a face from the sides, we return the face and None.

            :return: a list of faces from joins and faces
        """

        # brep vertices to cloud
        df_cloud = diffCheck.diffcheck_bindings.dfb_geometry.DFPointCloud()
        df_cloud.points = [np.array([vertex.Location.X, vertex.Location.Y, vertex.Location.Z]).reshape(3, 1) for vertex in self.brep.Vertices]
        if is_cylinder_beam:
            cylinder = self.find_largest_cylinder()
            Bounding_geometry = cylinder
        else:
            Bounding_geometry = diffCheck.df_cvt_bindings.cvt_dfOBB_2_rhbrep(df_cloud.get_tight_bounding_box())

        # scale the bounding geometry in the longest edge direction by 1.5 from center on both directions
        rh_Bounding_geometry_center = Bounding_geometry.GetBoundingBox(True).Center
        edges = Bounding_geometry.Edges
        edge_lengths = [edge.GetLength() for edge in edges]
        longest_edge = edges[edge_lengths.index(max(edge_lengths))]

        rh_Bounding_geometry_zaxis = rg.Vector3d(longest_edge.PointAt(1) - longest_edge.PointAt(0))
        rh_Bounding_geometry_plane = rg.Plane(rh_Bounding_geometry_center, rh_Bounding_geometry_zaxis)
        scale_factor = 0.1
        xform = rg.Transform.Scale(
            rh_Bounding_geometry_plane,
            1 - scale_factor,
            1 - scale_factor,
            1 + scale_factor
        )
        Bounding_geometry.Transform(xform)

        # check if face's centers are inside the OBB
        '''
        the structure of the disctionnary is as follows:
        {
            face_id: (face, is_inside)
            ...
        }
            face_id is int
            face is Rhino.Geometry.BrepFace
            is_inside is bool
        '''
        faces = {}
        if is_cylinder_beam:
            for idx, face in enumerate(self.brep.Faces):
                faces[idx] = (face, face.IsPlanar(1000 * sc.doc.ModelAbsoluteTolerance))
        else:
            for idx, face in enumerate(self.brep.Faces):
                face_centroid = rg.AreaMassProperties.Compute(face).Centroid
                coord = face.ClosestPoint(face_centroid)
                projected_centroid = face.PointAt(coord[1], coord[2])
                faces[idx] = (face, Bounding_geometry.IsPointInside(projected_centroid, sc.doc.ModelAbsoluteTolerance, True))

        # compute the adjacency list of each face
        adjacency_of_faces = {}
        '''
        the structure of the dictionnary is as follows:
        {
            face_id: (face, [adj_face_id_1, adj_face_id_2, ...])
            ...
        }
            face_id is int
            face is Rhino.Geometry.BrepFace
            adj_face_id_1, adj_face_id_2, ... are int
        '''
        for idx, face in faces.items():
            if not face[1]:
                continue
            adjacency_of_faces[idx] = (face[0], [adj_face for adj_face in face[0].AdjacentFaces() if faces[adj_face][1] and faces[adj_face][0].IsPlanar(1000 * sc.doc.ModelAbsoluteTolerance) and adj_face != idx]) # used to be not faces[adj_face][0].IsPlanar(1000 * sc.doc.ModelAbsoluteTolerance)
        adjacency_of_faces = diffCheck.df_util.merge_shared_indexes(adjacency_of_faces)
        joint_face_ids = [[key] + value[1] for key, value in adjacency_of_faces.items()]

        # get the proximity faces of the joint faces
        face_ids = self._assign_ids(joint_face_ids)

        self._faces = [(face, face_ids[idx]) for idx, face in enumerate(self.brep.Faces)]

        return self._faces
