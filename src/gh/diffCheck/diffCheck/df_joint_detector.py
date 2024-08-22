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

    def run(self):
        """
            Run the joint detector. We use a dictionary to store the faces of the cuts based wethear they are cuts or holes.
            - for cuts: If it is a cut we return the face, and the id of the joint the faces belongs to.
            - for sides: If it is a face from the sides, we return the face and None.

            :return: a list of faces from joins and faces
        """
        # brep vertices to cloud
        df_cloud = diffCheck.diffcheck_bindings.dfb_geometry.DFPointCloud()
        df_cloud.points = [np.array([vertex.Location.X, vertex.Location.Y, vertex.Location.Z]).reshape(3, 1) for vertex in self.brep.Vertices]

        rh_OBB = diffCheck.df_cvt_bindings.cvt_dfOBB_2_rhbrep(df_cloud.get_tight_bounding_box())

        # scale the box in the longest edge direction by 1.5 from center on both directions
        rh_OBB_center = rh_OBB.GetBoundingBox(True).Center
        edges = rh_OBB.Edges
        edge_lengths = [edge.GetLength() for edge in edges]
        longest_edge = edges[edge_lengths.index(max(edge_lengths))]

        rh_OBB_zaxis = rg.Vector3d(longest_edge.PointAt(1) - longest_edge.PointAt(0))
        rh_OBB_plane = rg.Plane(rh_OBB_center, rh_OBB_zaxis)
        scale_factor = 0.09
        xform = rg.Transform.Scale(
            rh_OBB_plane,
            1 - scale_factor,
            1 - scale_factor,
            1 + scale_factor
        )
        rh_OBB.Transform(xform)

        # check if face's centers are inside the OBB
        faces = {idx: (face, rh_OBB.IsPointInside(rg.AreaMassProperties.Compute(face).Centroid, sc.doc.ModelAbsoluteTolerance, True)) for idx, face in enumerate(self.brep.Faces)}

        # get the proximity faces of the joint faces
        joint_face_ids = [[key] + [adj_face for adj_face in value[0].AdjacentFaces() if faces[adj_face][1] and adj_face != key] for key, value in faces.items() if value[1]]

        face_ids = self._assign_ids(joint_face_ids)

        self._faces = [(face, face_ids[idx]) for idx, face in enumerate(self.brep.Faces)]

        return self._faces
