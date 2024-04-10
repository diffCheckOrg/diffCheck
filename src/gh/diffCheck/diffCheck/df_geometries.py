import os
from datetime import datetime
from dataclasses import dataclass
import typing
import uuid

import Rhino
import Rhino.Geometry as rg

import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

from df_joint_detector import JointDetector


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

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        if isinstance(other, DFVertex):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

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


@dataclass
class DFFace:
    """
    This class represents a face, in diffCheck, a face is a collection of vertices
    """
    outer_loop : typing.List[DFVertex]
    inner_loops : typing.List[typing.List[DFVertex]]
    joint_id : int
    def __post_init__(self):
        if len(self.outer_loop) < 3:
            raise ValueError("A face must have at least 3 vertices")
        self.outer_loop = self.outer_loop
        self.inner_loops = self.inner_loops or []

        self.joint_id = self.joint_id or None
        self.__is_joint = False
        self.__id = uuid.uuid4().int

        self._hastenonmortise = len(self.inner_loops) > 0

        self._brepface : rg.BrepFace = None

    def __repr__(self):
        return f"Face vertices: {len(self.outer_loop)}, Joint: {self.joint_id}, Inner loops: {len(self.inner_loops)}"

    def __hash__(self):
        outer_loop = tuple(tuple(vertex.__dict__.values()) for vertex in self.outer_loop)
        inner_loops = tuple(tuple(tuple(vertex.__dict__.values()) for vertex in loop) for loop in self.inner_loops)
        return hash((outer_loop, inner_loops))

    def __eq__(self, other):
        if isinstance(other, DFFace):
            is_outer_loop_equal = self.outer_loop == other.outer_loop
            is_inner_loops_equal = self.inner_loops == other.inner_loops
            return is_outer_loop_equal and is_inner_loops_equal
        return False

    @staticmethod
    def compute_mass_center(face: rg.BrepFace) -> rg.Point3d:
        """
        Compute the mass center of a  face

        :param face: The face to compute the mass center from
        :return mass_center: The mass center of the face
        """
        amp = rg.AreaMassProperties.Compute(face)
        if amp:
            return amp.Centroid
        return None

    @classmethod
    def from_brep(cls, brep_face: rg.BrepFace, joint_id: int=None):
        """
        Create a DFFace from a Rhino Brep face

        :param brep_face: The Rhino Brep face
        :param joint_id: The joint id
        :return face: The DFFace object
        """
        outer_loop = []

        face_loop = brep_face.OuterLoop
        face_loop_trims = face_loop.Trims

        face_curve_loop = brep_face.OuterLoop.To3dCurve()
        face_curve_loop = face_curve_loop.ToNurbsCurve()
        face_vertices = face_curve_loop.Points

        for f_v in face_vertices:
            vertex = DFVertex(f_v.X, f_v.Y, f_v.Z)
            outer_loop.append(vertex)
        
        inner_loops = []

        if brep_face.Loops.Count > 1:
            face_loops = brep_face.Loops
            for idx, loop in enumerate(face_loops):
                loop_trims = loop.Trims
                loop_curve = loop.To3dCurve()
                loop_curve = loop_curve.ToNurbsCurve()
                loop_vertices = loop_curve.Points
                inner_loop = []
                for l_v in loop_vertices:
                    vertex = DFVertex(l_v.X, l_v.Y, l_v.Z)
                    inner_loop.append(vertex)
                inner_loops.append(inner_loop)

        df_face = cls(outer_loop, inner_loops, joint_id)
        df_face._brepface = brep_face

        return df_face

    def to_brep(self):
        """
        Convert the face to a Rhino Brep planar face

        :return brep_face: The Rhino Brep planar face
        """
        # if the DFace was created from a brep face, return the brep face
        if self._brepface is not None:
            return self._brepface

        # FIXME: the rebuilding of breps with multiple loops is not working yet
        outer_vertices : rg.Point3d = [rg.Point3d(vertex.x, vertex.y, vertex.z) for vertex in self.outer_loop]
        outer_polyline = rg.Polyline(outer_vertices)
        outer_curve = outer_polyline.ToNurbsCurve()
        outer_curve = rg.Curve.CreateControlPointCurve(outer_vertices, 1)
        trim_loops.append(outer_curve)
        outer_brep = rg.Brep.CreatePlanarBreps(outer_curve, Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance)[0]

        return outer_brep

    @property
    def is_joint(self):
        if self.joint_id is not None:
            self.__is_joint = True
            return True
        self.__is_joint = False
        return False

    @property
    def id(self):
        return self.__id

    @property
    def has_tenonmortise(self):
        self._hastenonmortise = len(self.inner_loops) > 0
        return self._hastenonmortise


@dataclass
class DFBeam:
    """
    This class represents a beam, in diffCheck, a beam is a collection of faces
    """
    name : str
    faces : typing.List[DFFace]
    def __post_init__(self):
        self.name = self.name or "Unnamed Beam"
        self.faces = self.faces or []
        self._joint_faces = []
        self._side_faces = []

        self.__id = uuid.uuid4().int

    @classmethod
    def from_brep(cls, brep):
        """
        Create a DFBeam from a RhinoBrep object.
        It also removes duplicates and creates a list of unique faces.
        """
        faces = JointDetector(brep).run()
        faces = list(set(faces))
        beam = cls("Beam", faces)
        return beam

    def __repr__(self):
        return f"Beam: {self.name}, Faces: {len(self.faces)}"

    @property
    def id(self):
        return self.__id

    @property
    def joint_faces(self):
        return [face for face in self.faces if face.is_joint]

    @property
    def side_faces(self):
        return [face for face in self.faces if not face.is_joint]


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

        self._all_jointfaces = []
        self._all_sidefaces = []

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
                outer_loop = []
                for vertex_elem in face_elem.findall("Vertex"):
                    vertex = DFVertex(
                        float(vertex_elem.get("x")),
                        float(vertex_elem.get("y")),
                        float(vertex_elem.get("z"))
                    )
                    outer_loop.append(vertex)
                face = DFFace(outer_loop)
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

    # FIXME: to be reworked
    def to_xml(self):
        """
        Dump the assembly to an XML file

        :return xml_string: The pretty XML string
        """
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
                for vertex in face.outer_loop:
                    vertex_elem = ET.SubElement(face_elem, "Vertex")
                    vertex_elem.set("x", str(vertex.x))
                    vertex_elem.set("y", str(vertex.y))
                    vertex_elem.set("z", str(vertex.z))
        tree = ET.ElementTree(root)
        xml_string = ET.tostring(root, encoding='unicode')
        dom = parseString(xml_string)
        pretty_xml = dom.toprettyxml()

        return pretty_xml

    def dump(self, pretty_xml : str, dir: str):
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
    def all_joint_faces(self):
        for beam in self.beams:
            self._all_jointfaces.extend(beam.joint_faces)
        return self._all_jointfaces

    @property
    def all_side_faces(self):
        for beam in self.beams:
            self._all_sidefaces.extend(beam.side_faces)
        return self._all_sidefaces