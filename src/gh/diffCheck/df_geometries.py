from dataclasses import dataclass
import typing
import uuid

import Rhino
import Rhino.Geometry as rg


@dataclass
class DFVertex:
    """
    This class represents a vertex, a simple container with 3 coordinates
    """
    x : float
    y : float
    z : float
    def __post_init__(self):
        self.x = self.x or 0.0
        self.y = self.y or 0.0
        self.z = self.z or 0.0

    def __repr__(self):
        return f"Vertex: X={self.x}, Y={self.y}, Z={self.z}"


@dataclass
class DFFace:
    """
    This class represents a face, in diffCheck, a face is a collection of vertices
    """
    vertices : typing.List[DFVertex]
    joint_id : int=None
    def __post_init__(self):
        if len(self.vertices) < 3:
            raise ValueError("A face must have at least 3 vertices")
        self.vertices = self.vertices or []

        self.joint_id = self.joint_id or None
        self._is_joint = None
        self._id = uuid.uuid4().int

    def __repr__(self):
        return f"Face vertices: {len(self.vertices)}"

    @property
    def is_joint(self):
        if self.joint_id:
            return True
        return False

    @property
    def id(self):
        return self._id


@dataclass
class DFBeam:
    """
    This class represents a beam, in diffCheck, a beam is a collection of faces
    """
    name : str
    faces : typing.List[DFFace]
    def __post_init__(self):
        self.name = self.name or "Unnamed Beam"

        try:
            self.faces = list(self.faces)
        except TypeError:
            raise ValueError("Faces must be of type List[Face]")
        self.faces = self.faces or []

        self._id = uuid.uuid4().int

    @classmethod
    def from_brep(cls, brep):
        """
        Create a Beam from a RhinoBrep object
        """
        faces : typing.List[DFFace] = []
        brep_faces = brep.Faces
        for brep_face in brep_faces:
            vertices = []
            face_loop = brep_face.OuterLoop
            face_loop_trims = face_loop.Trims
            vertices : typing.List[DFVertex] = []
            for face_loop_trim in face_loop_trims:
                vertices.append(DFVertex(
                    face_loop_trim.Edge.PointAtStart.X,
                    face_loop_trim.Edge.PointAtStart.Y, 
                    face_loop_trim.Edge.PointAtStart.Z))
            faces.append(DFFace(vertices))
        beam = cls("Beam", faces)
        return beam

    def __repr__(self):
        return f"Beam: {self.name}, Faces: {len(self.faces)}"

    @property
    def id(self):
        return self._id


@dataclass
class DFAssembly:
    """
    This class represents an assembly of beams
    """
    beams : typing.List[DFBeam]
    name : str
    def __post_init__(self):
        self.beams = self.beams
        self.name = self.name or "Unnamed Assembly"

    def __repr__(self):
        return f"Assembly: {self.name}, Beams: {len(self.beams)}"

    def add_beam(self, beam: DFBeam):
        self.beams.append(beam)

    def remove_beam(self, beam_id: int):
        self.beams = [beam for beam in self.beams if beam.id != beam_id]