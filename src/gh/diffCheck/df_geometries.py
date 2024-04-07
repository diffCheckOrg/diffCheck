import os
from datetime import datetime
from dataclasses import dataclass
import typing
import uuid

import Rhino
import Rhino.Geometry as rg

import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString


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
        self.__is_joint = False
        self.__id = uuid.uuid4().int

    def __repr__(self):
        return f"Face vertices: {len(self.vertices)}"

    @property
    def is_joint(self):
        if self.joint_id:
            self.__is_joint = True
            return True
        self.__is_joint = False
        return False

    @property
    def id(self):
        return self.__id


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

        self.__id = uuid.uuid4().int

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
        return self.__id


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

    @classmethod
    def from_xml(cls, file_path: str):
        """
        Create an assembly from an XML file

        :param file_path: The path to the XML file
        :return assembly: The assembly object
        """
        # parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        beams : typing.List[DFBeam] = []
        
        name = root.get("name")
        for beam_elem in root.findall("Beam"):
            beam = DFBeam(beam_elem.get("name"), [])
            beam._DFBeam__id = int(beam_elem.get("id"))
            for face_elem in beam_elem.findall("Face"):
                vertices = []
                for vertex_elem in face_elem.findall("Vertex"):
                    vertex = DFVertex(
                        float(vertex_elem.get("x")),
                        float(vertex_elem.get("y")),
                        float(vertex_elem.get("z"))
                    )
                    vertices.append(vertex)
                face = DFFace(vertices)
                face._DFFace__id = int(face_elem.get("id"))
                face._DFFace__is_joint = bool(face_elem.get("is_joint"))
                face_joint : str = face_elem.get("joint_id")
                if face_joint != "None":
                    face.joint_id = int(face_joint)
                else:
                    face.joint_id = None
                beam.faces.append(face)
            beams.append(beam)
        return cls(beams, name)

    def dump_to_xml(self, dir: str):
        """
        Dump the assembly to an XML file

        :param dir: The directory to save the XML file
        :return xml_string: The pretty XML string
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        timestamp = "0"
        file_path = os.path.join(dir, f"{self.name}_{timestamp}.xml")

        root = ET.Element("Assembly")
        root.set("name", self.name)
        # dfbeams
        for beam in self.beams:
            beam_elem = ET.SubElement(root, "Beam")
            beam_elem.set("name", beam.name)
            beam_elem.set("id", str(beam.id))
            # dffaces
            for face in beam.faces:
                face_elem = ET.SubElement(beam_elem, "Face")
                face_elem.set("id", str(face.id))
                face_elem.set("is_joint", str(face.is_joint))
                face_elem.set("joint_id", str(face.joint_id))
                # dfvertices
                for vertex in face.vertices:
                    vertex_elem = ET.SubElement(face_elem, "Vertex")
                    vertex_elem.set("x", str(vertex.x))
                    vertex_elem.set("y", str(vertex.y))
                    vertex_elem.set("z", str(vertex.z))
        tree = ET.ElementTree(root)
        xml_string = ET.tostring(root, encoding='unicode')
        dom = parseString(xml_string)
        pretty_xml = dom.toprettyxml()
        with open(file_path, 'w') as f:
            f.write(pretty_xml)

        return pretty_xml