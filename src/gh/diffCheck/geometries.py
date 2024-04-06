#! python3
from dataclasses import dataclass
import typing
import uuid

@dataclass
class Face:
    """
    This class represents a face
    """
    name : str
    joint_id : int
    def __post_init__(self):
        self.name = self.name or "Unnamed Face"
        self.joint_id = self.joint_id or None
        self._is_joint = False
        self._id = uuid.uuid4().int

    @property
    def is_joint(self):
        if self.joint_id:
            return True
        return False

    @property
    def id(self):
        return self._id

@dataclass
class Beam:
    """
    This class represents a beam, in diffCheck, a beam is a collection of faces
    """
    name : str
    faces : typing.List[Face]

    def __post_init__(self):
        self.name = self.name or "Unnamed Beam"
        self.faces = self.faces or []
        self._has_joint = False
        self._id = uuid.uuid4().int

    @property
    def id(self):
        return self._id

@dataclass
class Assembly:
    """
    This class represents an assembly of beams
    """
    beams : typing.List[Beam]
    name : str
    def __post_init__(self):
        self.beams = self.beams or []
        self.name = self.name or "Unnamed Assembly"

    def add_beam(self, beam: Beam):
        self.beams.append(beam)

    def remove_beam(self, beam_id: int):
        self.beams = [beam for beam in self.beams if beam.id != beam_id]