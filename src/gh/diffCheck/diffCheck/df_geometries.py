import os
from datetime import datetime
from dataclasses import dataclass

import typing
from typing import Optional

import uuid

import Rhino
import Rhino.Geometry as rg
from Rhino.FileIO import SerializationOptions

from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

import diffCheck.df_joint_detector
import diffCheck.df_util

@dataclass
class DFVertex:
    """
    This class represents a vertex, a simple container with 3 coordinates
    """

    x: float
    y: float
    z: float

    def __post_init__(self):
        self.x = self.x or 0.0
        self.y = self.y or 0.0
        self.z = self.z or 0.0

        self.__uuid = uuid.uuid4().int

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state: typing.Dict):
        self.__dict__.update(state)

    def __repr__(self):
        return f"DFVertex: X={self.x}, Y={self.y}, Z={self.z}"

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        if isinstance(other, DFVertex):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def deepcopy(self):
        return DFVertex(self.x, self.y, self.z)

    @classmethod
    def from_rg_point3d(cls, point: rg.Point3d):
        """
        Create a DFVertex from a Rhino Point3d object

        :param point: The Rhino Point3d object
        :return vertex: The DFVertex object
        """
        return cls(point.X, point.Y, point.Z)

    def to_rg_point3d(self):
        """
        Convert the vertex to a Rhino Point3d object

        :return point: The Rhino Point3d object
        """
        return rg.Point3d(self.x, self.y, self.z)

    @property
    def uuid(self):
        return self.__uuid


@dataclass
class DFFace:
    """
    This class represents a face, in diffCheck, a face is a collection of vertices.
    """

    # just as breps a first outer loop and then inner loops of DFVertices
    all_loops: typing.List[typing.List[DFVertex]]
    joint_id: Optional[int] = None

    def __post_init__(self):
        self.all_loops: typing.List[typing.List[DFVertex]] = self.all_loops
        self.joint_id: Optional[int] = self.joint_id
        self.__is_joint = False
        self.__uuid = uuid.uuid4().int
        # if df_face is created from a rhino brep face, we store the rhino brep face
        self._rh_brepface: rg.BrepFace = None
        self.is_roundwood = False
        self._center: DFVertex = None
        # the normal of the face
        self._normal: typing.List[float] = None

    def __getstate__(self):
        state = self.__dict__.copy()
        if "all_loops" in state and state["all_loops"] is not None:
            state["all_loops"] = [[vertex.__getstate__() for vertex in loop] for loop in state["all_loops"]]
        # note: rg.BrepFaces cannot be serialized, so we need to convert it to a Surface >> JSON >> brep >> brepface (and vice versa)
        if "_rh_brepface" in state and state["_rh_brepface"] is not None:
            state["_rh_brepface"] = self.to_brep_face().DuplicateFace(True).ToJSON(SerializationOptions())
        if "_center" in state and state["_center"] is not None:
            state["_center"] = state["_center"].__getstate__()
        return state

    def __setstate__(self, state: typing.Dict):
        if "all_loops" in state and state["all_loops"] is not None:
            all_loops = []
            for loop_state in state["all_loops"]:
                loop = [DFVertex.__new__(DFVertex) for _ in loop_state]
                for vertex, vertex_state in zip(loop, loop_state):
                    vertex.__setstate__(vertex_state)
                all_loops.append(loop)
            state["all_loops"] = all_loops
        if "_center" in state and state["_center"] is not None:
            state["_center"] = DFVertex.__new__(DFVertex).__setstate__(state["_center"])
        # note: rg.BrepFaces cannot be serialized, so we need to convert it to a Surface >> JSON >> brep >> brepface (and vice versa)
        if "_rh_brepface" in state and state["_rh_brepface"] is not None:
            state["_rh_brepface"] = rg.Surface.FromJSON(state["_rh_brepface"]).Faces[0]
        self.__dict__.update(state)
        if self._rh_brepface is not None:
            self.from_brep_face(self._rh_brepface, self.joint_id)

    def __repr__(self):
        return f"Face id: {(self.id)}, IsJoint: {self.is_joint} Loops: {len(self.all_loops)}"

    def __hash__(self):
        outer_loop = tuple(
            tuple(vertex.__dict__.values()) for vertex in self.all_loops[0]
        )
        inner_loops = tuple(
            tuple(vertex.__dict__.values())
            for loop in self.all_loops[1:]
            for vertex in loop
        )
        return hash((outer_loop, inner_loops))

    def __eq__(self, other):
        if isinstance(other, DFFace):
            # check if
            return self.all_loops == other.all_loops
        return False

    def deepcopy(self):
        loop_copy: typing.List[typing.List[DFVertex]] = []
        for loop in self.all_loops:
            loop_copy.append([vertex.deepcopy() for vertex in loop])
        return DFFace(loop_copy, self.joint_id)

    @classmethod
    def from_brep_face(cls,
        brep_face: rg.BrepFace,
        joint_id: Optional[int] = None):
        """
        Create a DFFace from a Rhino Brep face

        :param brep_face: The Rhino Brep face
        :param joint_id: The joint id
        :return face: The DFFace object
        """
        all_loops = []
        df_face: DFFace = cls([], joint_id)

        for idx, loop in enumerate(brep_face.Loops):
            loop_curve = loop.To3dCurve()
            loop_curve = loop_curve.ToNurbsCurve()
            loop_vertices = loop_curve.Points
            loop = []
            for l_v in loop_vertices:
                vertex = DFVertex(l_v.X, l_v.Y, l_v.Z)
                loop.append(vertex)
            all_loops.append(loop)

        df_face = cls(all_loops, joint_id)
        df_face._rh_brepface = brep_face

        return df_face

    def to_brep_face(self):
        """
        Convert the face to a Rhino Brep planar face

        :return brep_face: The Rhino Brep planar face
        """
        if self._rh_brepface is not None:
            return self._rh_brepface

        if self.is_roundwood:
            ghenv.Component.AddRuntimeMessage(  # noqa: F821
                RML.Warning, "The DFFace was a cylinder created from scratch \n \
                 , it cannot convert to brep.")

        brep_curves = []

        for loop in self.all_loops:
            inner_vertices = [
                rg.Point3d(vertex.x, vertex.y, vertex.z) for vertex in loop
            ]
            inner_polyline = rg.Polyline(inner_vertices)
            inner_curve = inner_polyline.ToNurbsCurve()
            brep_curves.append(inner_curve)

        brep = rg.Brep.CreatePlanarBreps(
            brep_curves, Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance
        )[0]

        return brep

    def to_mesh(self):
        """
        Convert the face to a Rhino Mesh

        :return mesh: The Rhino Mesh object
        """
        mesh = Rhino.Geometry.Mesh()

        mesh_parts = Rhino.Geometry.Mesh.CreateFromBrep(
                self.to_brep_face().DuplicateFace(True),
                Rhino.Geometry.MeshingParameters.QualityRenderMesh)

        for mesh_part in mesh_parts:
            mesh.Append(mesh_part)
        mesh.Faces.ConvertQuadsToTriangles()
        # mesh.Compact()

        return mesh

    @property
    def is_joint(self):
        if self.joint_id is not None:
            self.__is_joint = True
            return True
        self.__is_joint = False
        return False

    @property
    def uuid(self):
        return self.__uuid

    @property
    def center(self):
        if self._center is None:
            vertices = [vertex.to_rg_point3d() for vertex in self.all_loops[0]]
            self._center = DFVertex.from_rg_point3d(rg.BoundingBox(vertices).Center)
        return self._center

    @property
    def normal(self):
        if self._normal is None:
            normal_rg = self.to_brep_face().NormalAt(0, 0)
            self._normal = [normal_rg.X, normal_rg.Y, normal_rg.Z]
        return self._normal

@dataclass
class DFJoint:
    """
    This class represents a joint, in diffCheck, a joint is a collection of faces
    For convenience, this is used only as a return type from the DFBeam class's property for retrieveing joints
    """

    id: int
    faces: typing.List[DFFace]

    def __post_init__(self):
        self.id = self.id
        self.faces = self.faces or []

        # this is an automatic identifier
        self.__uuid = uuid.uuid4().int
        # the center from the AABB of the joint
        self._center: DFVertex = None
        self.distance_to_beam_midpoint: float = None

    def __getstate__(self):
        state = self.__dict__.copy()
        if "faces" in state and state["faces"] is not None:
            state["faces"] = [face.__getstate__() for face in self.faces]
        if "_center" in state and state["_center"] is not None:
            state["_center"] = state["_center"].__getstate__()
        return state

    def __setstate__(self, state: typing.Dict):
        if "faces" in state and state["faces"] is not None:
            faces = []
            for face_state in state["faces"]:
                face = DFFace.__new__(DFFace)
                face.__setstate__(face_state)
                faces.append(face)
            state["faces"] = faces
        if "_center" in state and state["_center"] is not None:
            state["_center"] = DFVertex.__new__(DFVertex).__setstate__(state["_center"])
        self.__dict__.update(state)

    def __repr__(self):
        return f"Joint id: {self.id}, Faces: {len(self.faces)}"

    def deepcopy(self):
        return DFJoint(self.id, self.faces.deepcopy())

    def to_brep(self):
        """
        Convert the joint to a Rhino Brep object
        """
        brep = rg.Brep()
        for face in self.faces:
            brep.Append(face.to_brep_face().ToBrep())
        brep.Compact()
        return brep

    def to_mesh(self, max_edge_length):
        """
        Convert the joint to a Rhino Mesh object
        """
        rhino_brep_faces = [f.to_brep_face() for f in self.faces]
        mesh = rg.Mesh()

        new_faces = [f.DuplicateFace(True) for f in rhino_brep_faces]

        for f in new_faces:
            param = rg.MeshingParameters()
            param.MaximumEdgeLength = max_edge_length
            mesh_part = rg.Mesh.CreateFromBrep(f, param)[0]
            mesh.Append(mesh_part)

        mesh.Faces.ConvertQuadsToTriangles()
        mesh.Compact()
        return mesh

    @property
    def uuid(self):
        """ It retrives the automatic identifier, not the one of the joint in the beam """
        return self.__uuid

    @property
    def center(self):
        if self._center is None:
            vertices = []
            for face in self.faces:
                vertices.extend(face.all_loops[0])
            vertices = [vertex.to_rg_point3d() for vertex in vertices]
            self._center = DFVertex.from_rg_point3d(rg.BoundingBox(vertices).Center)
        return self._center


@dataclass
class DFBeam:
    """
    This class represents a beam, in diffCheck, a beam is a collection of faces
    """

    name: str
    faces: typing.List[DFFace]

    def __post_init__(self):
        self.name: str = self.name or "Unnamed Beam"
        self.faces: typing.List[DFFace] = self.faces or []
        self.is_roundwood: bool = False

        self._joint_faces: typing.List[DFFace] = []
        self._side_faces: typing.List[DFFace] = []
        self._vertices: typing.List[DFVertex] = []
        self._joints: typing.List[DFJoint] = []

        self._index_assembly: int = None

        self._center: rg.Point3d = None
        self._axis: rg.Line = self.compute_axis()
        self._length: float = self._axis.Length

        self.__uuid = uuid.uuid4().int
        self.__id = uuid.uuid4().int


    def __getstate__(self):
        state = self.__dict__.copy()
        if "faces" in state and state["faces"] is not None:
            state["faces"] = [face.__getstate__() for face in self.faces]
        if "_joint_faces" in state and state["_joint_faces"] is not None:
            state["_joint_faces"] = [face.__getstate__() for face in state["_joint_faces"]]
        if "_side_faces" in state and state["_side_faces"] is not None:
            state["_side_faces"] = [face.__getstate__() for face in state["_side_faces"]]
        if "_vertices" in state and state["_vertices"] is not None:
            state["_vertices"] = [vertex.__getstate__() for vertex in state["_vertices"]]
        if "_joints" in state and state["_joints"] is not None:
            state["_joints"] = [joint.__getstate__() for joint in state["_joints"]]
        if "_axis" in state and state["_axis"] is not None:
            state["_axis"] = [
                state["_axis"].From.X,
                state["_axis"].From.Y,
                state["_axis"].From.Z,
                state["_axis"].To.X,
                state["_axis"].To.Y,
                state["_axis"].To.Z
            ]
        if "_center" in state and state["_center"] is not None:
            state["_center"] = DFVertex(self._center.X, self._center.Y, self._center.Z).__getstate__()
        return state

    def __setstate__(self, state: typing.Dict):
        if "faces" in state and state["faces"] is not None:
            faces = []
            for face_state in state["faces"]:
                face = DFFace.__new__(DFFace)
                face.__setstate__(face_state)
                faces.append(face)
            state["faces"] = faces
        if "_joint_faces" in state and state["_joint_faces"] is not None:
            joint_faces = []
            for face_state in state["_joint_faces"]:
                face = DFFace.__new__(DFFace)
                face.__setstate__(face_state)
                joint_faces.append(face)
            state["_joint_faces"] = joint_faces
        if "_side_faces" in state and state["_side_faces"] is not None:
            side_faces = []
            for face_state in state["_side_faces"]:
                face = DFFace.__new__(DFFace)
                face.__setstate__(face_state)
                side_faces.append(face)
            state["_side_faces"] = side_faces
        if "_vertices" in state and state["_vertices"] is not None:
            vertices = []
            for vertex_state in state["_vertices"]:
                vertex = DFVertex.__new__(DFVertex)
                vertex.__setstate__(vertex_state)
                vertices.append(vertex)
            state["_vertices"] = vertices
        if "_joints" in state and state["_joints"] is not None:
            joints = []
            for joint_state in state["_joints"]:
                joint = DFJoint.__new__(DFJoint)
                joint.__setstate__(joint_state)
                joints.append(joint)
            state["_joints"] = joints
        if "_axis" in state and state["_axis"] is not None:
            state["_axis"] = rg.Line(
                rg.Point3d(state["_axis"][0], state["_axis"][1], state["_axis"][2]),
                rg.Point3d(state["_axis"][3], state["_axis"][4], state["_axis"][5])
            )
        if "_center" in state and state["_center"] is not None:
            center = DFVertex.__new__(DFVertex)
            center.__setstate__(state["_center"])
            state["_center"] = rg.Point3d(center.x, center.y, center.z)
        self.__dict__.update(state)

    def __repr__(self):
        return f"Beam: {self.name}, Faces: {len(self.faces)}"

    def deepcopy(self):
        return DFBeam(self.name, [face.deepcopy() for face in self.faces])

    def compute_axis(self, is_unitized: bool = True) -> rg.Line:
        """
        This is an utility function that computes the axis of the beam as a line.
        The axis is calculated as the vector passing through the two most distance joint's centroids.

        :return axis: The axis of the beam as a line
        """
        joints = self.joints
        joint1 = None
        joint2 = None
        if len(joints) > 2:
            joint1 = joints[0]
            joint2 = joints[1]
            max_distance = 0
            for j1 in joints:
                for j2 in joints:
                    distance = rg.Point3d.DistanceTo(
                        j1.center.to_rg_point3d(),
                        j2.center.to_rg_point3d())
                    if distance > max_distance:
                        max_distance = distance
                        joint1 = j1
                        joint2 = j2
        else:
            #get the two farthest dffaces for simplicity
            df_faces = [face for face in self.faces]
            max_distance = 0
            for i in range(len(df_faces)):
                for j in range(i+1, len(df_faces)):
                    distance = rg.Point3d.DistanceTo(
                        df_faces[i].center.to_rg_point3d(),
                        df_faces[j].center.to_rg_point3d())
                    if distance > max_distance:
                        max_distance = distance
                        joint1 = df_faces[i]
                        joint2 = df_faces[j]

        if joint1 is None or joint2 is None:
            raise ValueError("The beam axis cannot be calculated")

        axis_ln = rg.Line(
            joint1.center.to_rg_point3d(),
            joint2.center.to_rg_point3d()
            )

        return axis_ln

    def compute_joint_distances_to_midpoint(self) -> typing.List[float]:
        """
            This function computes the distances from the center of the beam to each joint.
        """
        def _project_point_to_line(point, line):
            """ Compute the projection of a point onto a line """

            line_start = line.From
            line_end = line.To
            line_direction = rg.Vector3d(line_end - line_start)

            line_direction.Unitize()

            vector_to_point = rg.Vector3d(point - line_start)
            dot_product = rg.Vector3d.Multiply(vector_to_point, line_direction)
            projected_point = line_start + line_direction * dot_product

            return projected_point

        distances = []
        for idx, joint in enumerate(self.joints):
            joint_ctr = joint.center.to_rg_point3d()
            ln = self.axis
            ln.Extend(self.axis.Length, self.axis.Length)

            projected_point = _project_point_to_line(joint_ctr, ln)

            dist = rg.Point3d.DistanceTo(
                self.center,
                projected_point
            )
            distances.append(dist)
        return distances

    def compute_joint_angles(self) -> typing.List[float]:
        """
        This function computes the angles between the beam's axis and the joints'jointfaces' normals.
        The angles are remapped between 0 and 90 degrees, where -1 indicates the bottom of any half-lap joint.

        :return angles: The angles between the beam's axis and the joints'jointfaces' normals
        """
        jointface_angles = []
        for joint in self.joints:
            jointfaces_angles = []
            for joint_face in joint.faces:
                joint_normal = joint_face.normal
                joint_normal = rg.Vector3d(joint_normal[0], joint_normal[1], joint_normal[2])
                angle = rg.Vector3d.VectorAngle(self.axis.Direction, joint_normal)
                angle_degree = Rhino.RhinoMath.ToDegrees(angle)
                jointfaces_angles.append(angle_degree)
                angle_degree = int(angle_degree)

                if angle_degree > 90:
                    angle_degree = 180 - angle_degree
                if angle_degree >= 89 and angle_degree <= 90:
                    angle_degree = -1

                jointface_angles.append(angle_degree)
        return jointface_angles

    @classmethod
    def from_brep_face(cls, brep, is_roundwood=False):
        """
        Create a DFBeam from a RhinoBrep object.
        It also removes duplicates and creates a list of unique faces.
        """
        faces : typing.List[DFFace] = []
        data_faces = diffCheck.df_joint_detector.JointDetector(brep, is_roundwood).run()
        for data in data_faces:
            face = DFFace.from_brep_face(data[0], data[1])
            faces.append(face)
        beam = cls("Beam", faces)
        beam.is_roundwood = is_roundwood
        return beam

    def to_brep(self):
        """
        Convert the beam to a Rhino Brep object
        """
        brep = rg.Brep()
        for face in self.faces:
            if isinstance(face.to_brep_face(), rg.Brep):
                brep.Append(face.to_brep_face())
            else:
                brep.Append(face.to_brep_face().ToBrep())
        brep.Compact()

        return brep

    def to_mesh(self, max_edge_length):
        """
        Convert the beam to a Rhino Mesh object
        """
        rhino_brep_faces = [f.to_brep_face() for f in self.faces]
        mesh = rg.Mesh()

        new_faces = [f.DuplicateFace(True) for f in rhino_brep_faces]  # .DuplicateFace bypasses the problem of untrimmed faces that appear in f.to_brep_face

        for f in new_faces:
            param = rg.MeshingParameters()
            param.MaximumEdgeLength = max_edge_length
            mesh_part = rg.Mesh.CreateFromBrep(f, param)[0] #returns a list of meshes with one element
            mesh.Append(mesh_part)

        mesh.Compact()
        return mesh

    @property
    def uuid(self):
        return self.__uuid

    @property
    def number_joints(self):
        return max([joint.id for joint in self.joints]) + 1

    @property
    def joint_faces(self):
        return [face for face in self.faces if face.is_joint]

    @property
    def side_faces(self):
        return [face for face in self.faces if not face.is_joint]

    @property
    def joints(self):
        joints : typing.List[DFJoint] = []
        temp_faces = self.joint_faces.copy()
        while len(temp_faces) > 0:
            joint_id = temp_faces[0].joint_id
            joint_faces = [face for face in temp_faces if face.joint_id == joint_id]
            joint = DFJoint(joint_id, joint_faces)
            joints.append(joint)
            temp_faces = [face for face in temp_faces if face.joint_id != joint_id]
        return joints

    @property
    def center(self):
        self._center = self.to_brep().GetBoundingBox(True).Center
        return self._center

    @property
    def index_assembly(self):
        if self._index_assembly is None:
            raise ValueError("The beam is not added to an assembly")
        return self._index_assembly

    @property
    def vertices(self):
        self._vertices = []
        for face in self.faces:
            all_loops_cpy = face.all_loops.copy()
            for loop in all_loops_cpy:
                self._vertices.extend(loop)
        return self._vertices

    @property
    def axis(self):
        self._axis = self.compute_axis()
        return self._axis

    @property
    def length(self):
        self._length = self._axis.Length
        return self._length

@dataclass
class DFAssembly:
    """
    This class represents an assembly of beams
    """

    beams: typing.List[DFBeam]
    name: str

    def __post_init__(self):
        self.beams: typing.List[DFBeam] = self.beams
        for idx, beam in enumerate(self.beams):
            beam._index_assembly = idx

        self.__uuid: int = uuid.uuid4().int

        self.name: str = self.name or "Unnamed Assembly"

        self._all_jointfaces: typing.List[DFFace] = []
        self._all_sidefaces: typing.List[DFFace] = []
        self._all_vertices: typing.List[DFVertex] = []
        self._all_joints: typing.List[DFJoint] = []

        self.contains_cylinders: bool = any(beam.is_roundwood for beam in self.beams)

        self._mass_center: rg.Point3d = None

        self._has_onle_one_beam: bool = False

    def __getstate__(self):
        state = self.__dict__.copy()
        if "beams" in state and state["beams"] is not None:
            state["beams"] = [beam.__getstate__() for beam in self.beams]
        if "_mass_center" in state and state["_mass_center"] is not None:
            state["_mass_center"] = self._mass_center.ToJSON(SerializationOptions())
        if "_all_jointfaces" in state and state["_all_jointfaces"] is not None:
            state["_all_jointfaces"] = [face.__getstate__() for face in state["_all_jointfaces"]]
        if "_all_sidefaces" in state and state["_all_sidefaces"] is not None:
            state["_all_sidefaces"] = [face.__getstate__() for face in state["_all_sidefaces"]]
        if "_all_vertices" in state and state["_all_vertices"] is not None:
            state["_all_vertices"] = [vertex.__getstate__() for vertex in state["_all_vertices"]]
        if "_all_joints" in state and state["_all_joints"] is not None:
            state["_all_joints"] = [joint.__getstate__() for joint in state["_all_joints"]]
        return state

    def __setstate__(self, state: typing.Dict):
        if "beams" in state and state["beams"] is not None:
            beams = []
            for beam_state in state["beams"]:
                beam = DFBeam.__new__(DFBeam)
                beam.__setstate__(beam_state)
                beams.append(beam)
            state["beams"] = beams
        if "_mass_center" in state and state["_mass_center"] is not None:
            state["_mass_center"] = rg.Point3d.FromJSON(state["_mass_center"])
        if "_all_jointfaces" in state and state["_all_jointfaces"] is not None:
            joint_faces = []
            for face_state in state["_all_jointfaces"]:
                face = DFFace.__new__(DFFace)
                face.__setstate__(face_state)
                joint_faces.append(face)
            state["_all_jointfaces"] = joint_faces
        if "_all_sidefaces" in state and state["_all_sidefaces"] is not None:
            side_faces = []
            for face_state in state["_all_sidefaces"]:
                face = DFFace.__new__(DFFace)
                face.__setstate__(face_state)
                side_faces.append(face)
            state["_all_sidefaces"] = side_faces
        if "_all_vertices" in state and state["_all_vertices"] is not None:
            vertices = []
            for vertex_state in state["_all_vertices"]:
                vertex = DFVertex.__new__(DFVertex)
                vertex.__setstate__(vertex_state)
                vertices.append(vertex)
            state["_all_vertices"] = vertices
        if "_all_joints" in state and state["_all_joints"] is not None:
            joints = []
            for joint_state in state["_all_joints"]:
                joint = DFJoint.__new__(DFJoint)
                joint.__setstate__(joint_state)
                joints.append(joint)
            state["_all_joints"] = joints
        self.__dict__.update(state)

    def __repr__(self):
        return f"Assembly: {self.name}, Beams: {len(self.beams)}"

    def deepcopy(self):
        """
        Create a deep copy of the assembly
        """
        beams = [beam.deepcopy() for beam in self.beams]
        return DFAssembly(beams, self.name)

    def add_beam(self, beam: DFBeam):
        beam._index_assembly = len(self.beams)
        self.beams.append(beam)

    def remove_beam(self, beam_assembly_index: int):
        """ Remove a beam from the assembly """
        for idx, beam in enumerate(self.beams):
            if beam.index_assembly == beam_assembly_index:
                self.beams.pop(idx)
                break

    def compute_all_joint_distances_to_midpoint(self) -> typing.List[float]:
        """
        This function computes the distances from the center of the assembly to each joint.
        """
        distances = []
        for beam in self.beams:
            distances.extend(beam.compute_joint_distances_to_midpoint())
        return distances

    def compute_all_joint_angles(self) -> typing.List[float]:
        """
        This function computes the angles between the beam's axis and the joints'jointfaces' normals.
        """
        angles = []
        for beam in self.beams:
            angles.extend(beam.compute_joint_angles())
        return angles

    def to_xml(self):
        """
        Dump the assembly's meshes to an XML file. On top of the DiffCheck datatypes and structure,
        we export the underlaying beams's meshes from Rhino as vertices and faces.

        :return xml_string: The pretty XML string
        """
        root = ET.Element("DFAssembly")
        root.set("name", self.name)
        # dfbeamsgra
        for beam in self.beams:
            beam_elem = ET.SubElement(root, "DFBeam")
            beam_elem.set("name", beam.name)
            beam_elem.set("id", str(beam.id))
            # dffaces
            for face in beam.faces:
                face_elem = ET.SubElement(beam_elem, "DFFace")
                face_elem.set("id", str(face.id))
                face_elem.set("is_joint", str(face.is_joint))
                face_elem.set("joint_id", str(face.joint_id))
                # export linked mesh
                facerhmesh_elem = ET.SubElement(face_elem, "RhMesh")
                mesh = face.to_mesh()
                mesh_vertices = mesh.Vertices
                for idx, vertex in enumerate(mesh_vertices):
                    facerhmesh_vertex_elem = ET.SubElement(
                        facerhmesh_elem, "RhMeshVertex"
                    )
                    facerhmesh_vertex_elem.set("x", str(vertex.X))
                    facerhmesh_vertex_elem.set("y", str(vertex.Y))
                    facerhmesh_vertex_elem.set("z", str(vertex.Z))
                mesh_faces = mesh.Faces
                for idx, face in enumerate(mesh_faces):
                    facerhmesh_face_elem = ET.SubElement(facerhmesh_elem, "RhMeshFace")
                    facerhmesh_face_elem.set("v1", str(face.A))
                    facerhmesh_face_elem.set("v2", str(face.B))
                    facerhmesh_face_elem.set("v3", str(face.C))
                    facerhmesh_face_elem.set("v4", str(face.D))

        xml_string = ET.tostring(root, encoding="unicode")
        dom = parseString(xml_string)
        pretty_xml = dom.toprettyxml()

        return pretty_xml

    def dump_xml(self, pretty_xml: str, dir: str):
        """
        Dump the pretty XML to a file

        :param pretty_xml: The pretty XML string
        :param dir: The directory to save the XML
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(dir, f"{self.name}_{timestamp}.xml")

        with open(file_path, "w") as f:
            f.write(pretty_xml)

    @property
    def total_number_joints(self):
        return max([joint.id for joint in self.all_joints]) + 1

    @property
    def all_joint_faces(self):
        self._all_jointfaces = []
        for beam in self.beams:
            self._all_jointfaces.extend(beam.joint_faces)
        return self._all_jointfaces

    @property
    def all_side_faces(self):
        self._all_sidefaces = []
        for beam in self.beams:
            self._all_sidefaces.extend(beam.side_faces)
        return self._all_sidefaces

    @property
    def all_joints(self):
        self._all_joints = []
        for beam in self.beams:
            self._all_joints.extend(beam.joints)
        return self._all_joints

    @property
    def all_vertices(self):
        self._all_vertices = []
        for beam in self.beams:
            for face in beam.faces:
                self._all_vertices.extend(face.all_loops[0])
        return self._all_vertices

    @property
    def mass_center(self):
        # calculate the mass center of the assembly
        df_vertices = self.all_vertices
        rh_vertices = [vertex.to_rg_point3d() for vertex in df_vertices]
        self._mass_center = rg.BoundingBox(rh_vertices).Center
        return self._mass_center

    @property
    def uuid(self):
        return self.__uuid

    @property
    def has_only_one_beam(self):
        if len(self.beams) == 1:
            self._has_onle_one_beam = True
        return self._has_onle_one_beam
