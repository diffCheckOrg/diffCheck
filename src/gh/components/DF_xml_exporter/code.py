#! python3
# r: diffCheck==0.0.8
# r: numpy

import System
import typing

import Rhino
import Rhino.Geometry as rg

from ghpythonlib.componentbase import executingcomponent as component

import diffCheck
from diffCheck.df_geometries import DFBeam, DFAssembly


class DFXMLExporter(component):
    def RunScript(self,
            i_dump: bool,
            i_assembly_name,
            i_export_dir,
            i_breps: System.Collections.Generic.IList[Rhino.Geometry.Brep]):
        """
            This read breps from Rhino, converts them to DFBeams and DFAssemblies, and exports them to XML.
            
            :param i_dump: whether to dump the xml
            :param i_export_dir: directory to export the xml
            :param i_breps: list of breps
        """
        # beams
        beams: typing.List[DFBeam] = []
        for brep in i_breps:
            beam = DFBeam.from_brep(brep)
            beams.append(beam)

        # assembly
        assembly1 = DFAssembly(beams, i_assembly_name)

        # dump the xml
        xml: str = assembly1.to_xml()
        if i_dump:
            assembly1.dump_xml(xml, i_export_dir)
        o_xml = xml

        # show the joint/side faces
        o_joints = [jf.to_brep() for jf in assembly1.all_joint_faces]
        o_sides = [sf.to_brep() for sf in assembly1.all_side_faces]

        return o_xml, o_joints, o_sides