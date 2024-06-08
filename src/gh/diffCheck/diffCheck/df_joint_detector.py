
import Rhino
import scriptcontext as sc
import Rhino.Geometry as rg

import typing
from dataclasses import dataclass

import diffCheck.df_util
import diffCheck.df_transformations

from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import numpy as np


@dataclass
class JointDetector:
    """
    This class is responsible for detecting joints in a brep
    """
    brep : Rhino.Geometry.Brep
    def __post_init__(self):
        self.brep = self.brep or None
        # list of straight cuts
        self._cuts : typing.List[rg.Brep] = []
        # list of holes
        self._holes : typing.List[rg.Brep] = []
        # list of mixed joints (cuts+holes)
        self._mix : typing.List[rg.Brep]= []

        # list of DFFaces from joints and sides
        self._faces = []

    def _compute_mass_center(self, b_face: rg.BrepFace) -> rg.Point3d:
        """
        Compute the mass center of a brep face
        :param b_face: The brep face to compute the mass center from
        :return mass_center: The mass center of the brep face
        """
        amp = rg.AreaMassProperties.Compute(b_face)
        if amp:
            return amp.Centroid
        return None

    def run(self) :
        """
            Run the joint detector. We use a dictionary to store the faces of the cuts based wethear they are cuts or holes.
            - for cuts: If it is a cut we return the face, and the id of the joint the faces belongs to.
            - for sides: If it is a face from the sides, we return the face and None.

            :return: a list of faces from joins and faces
        """
        # brep vertices to cloud
        df_cloud = diffCheck.diffcheck_bindings.dfb_geometry.DFPointCloud()
        brep_vertices = []
        for vertex in self.brep.Vertices:
            brep_vertices.append(np.array([vertex.Location.X, vertex.Location.Y, vertex.Location.Z]).reshape(3, 1))
        df_cloud.points = brep_vertices

        df_OBB = df_cloud.get_tight_bounding_box()
        rh_OBB = diffCheck.df_cvt_bindings.cvt_dfOBB_2_rhbrep(df_OBB)

        # scale the box in the longest edge direction by 1.5 from center on both directions
        rh_OBB_center = rh_OBB.GetBoundingBox(True).Center
        edges = rh_OBB.Edges
        edge_lengths = [edge.GetLength() for edge in edges]
        longest_edge = edges[edge_lengths.index(max(edge_lengths))]
        shortest_edge = edges[edge_lengths.index(min(edge_lengths))]

        rh_OBB_zaxis = rg.Vector3d(longest_edge.PointAt(1) - longest_edge.PointAt(0))
        rh_OBB_plane = rg.Plane(rh_OBB_center, rh_OBB_zaxis)
        scale_factor = 0.09
        xform = rg.Transform.Scale(
            rh_OBB_plane,
            1-scale_factor,
            1-scale_factor,
            1+scale_factor
        )
        rh_OBB.Transform(xform)

        # check if face's centers are inside the OBB
        faces = {}
        for idx, face in enumerate(self.brep.Faces):
            face_center = rg.AreaMassProperties.Compute(face).Centroid
            if rh_OBB.IsPointInside(face_center, sc.doc.ModelAbsoluteTolerance, True):
                faces[idx] = (face, True)
            else:
                faces[idx] = (face, False)

        face_jointid = {}  # face : joint id (int) or None
        joint_counter = 0
        for key, value in faces.items():
            if value[1]:
                face_jointid[key] = joint_counter
                adjacent_faces = value[0].AdjacentFaces()
                for adj_face in adjacent_faces:
                    if faces[adj_face][1]:
                        face_jointid[value] = joint_counter
                joint_counter += 1
            else:
                face_jointid[value] = None

        o_sides = [faces[key][0] for key, value in faces.items() if not value[1]]
        o_joints = [faces[key][0] for key, value in faces.items() if value[1]]

        # create the faces
        # self._faces = [(face, face_jointid[idx]) for idx, face in faces.items()]
        # self._faces = [DFFace.from_brep(face, face_jointid[idx]) for idx, face in faces.items()]

        return self._faces