#! python3
# requirements: diffCheck
"""
This read breps from Rhino, converts them to DFBeams and DFAssemblies, and exports them to XML.

:param i_breps: list of breps
:param i_export_dir: directory to export the xml
:param i_dump: press to dump the xml
"""
import System
import typing

import Rhino
import Rhino.Geometry as rg

from ghpythonlib.componentbase import executingcomponent as component

from diffCheck.df_geometries import DFVertex, DFFace, DFBeam, DFAssembly


class DFXMLExporter(component):
    def RunScript(self,
                  i_dump : bool,
                  i_name : str,
                  i_export_dir : str,
                  i_breps : typing.List[Rhino.Geometry.Brep]
                  ):
        """
        Main function to test the package
        :param i_dump: whether to dump the xml
        :param i_export_dir: directory to export the xml
        :param i_breps: list of breps
        """
        # beams
        beams : typing.List[DFBeam] = []
        for brep in i_breps:
            beam = DFBeam.from_brep(brep)
            beams.append(beam)

        # assembly
        assembly1 = DFAssembly(beams, i_name)
        print(assembly1.beams)
        print(assembly1)

        # dump the xml
        xml : str = assembly1.to_xml()
        if i_dump:
            assembly1.dump(xml, i_export_dir)
        o_xml = xml

        return o_xml