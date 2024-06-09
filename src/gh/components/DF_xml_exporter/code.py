#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
import scriptcontext as sc

from ghpythonlib.componentbase import executingcomponent as component

import diffCheck
from diffCheck.df_geometries import DFBeam, DFAssembly
import diffCheck.df_transformations

import diffCheck.diffcheck_bindings
import diffCheck.df_cvt_bindings

import diffCheck.df_joint_detector
import diffCheck.df_geometries


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
        ################
        o_xml = None
        o_joints = None
        o_sides = None
        o_debug = None
        ################
        ########################################

        # beams
        beams: typing.List[DFBeam] = []
        for brep in i_breps:
            beam = DFBeam.from_brep_face(brep)
            beams.append(beam)

        # assembly
        assembly1 = DFAssembly(beams, i_assembly_name)

        # dump the xml
        xml: str = assembly1.to_xml()
        if i_dump:
            assembly1.dump_xml(xml, i_export_dir)
        o_xml = xml

        # show the joint/side faces
        o_joints = [jf.to_brep_face() for jf in assembly1.all_joint_faces]
        o_sides = [sf.to_brep_face() for sf in assembly1.all_side_faces]

        return o_xml, o_joints, o_sides, o_debug


if __name__ == "__main__":
    com = DFXMLExporter()
    o_xml, o_joints, o_sides, o_debug = com.RunScript(
        i_dump,
        i_assembly_name,
        i_export_dir,
        i_breps
    )