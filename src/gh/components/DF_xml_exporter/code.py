#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
import scriptcontext as sc

from ghpythonlib.componentbase import executingcomponent as component


class DFXMLExporter(component):
    def RunScript(self,
            i_dump: bool,
            i_export_dir,
            i_assembly):
        # dump the xml
        o_xml = None
        xml: str = i_assembly.to_xml()
        if i_dump:
            i_assembly.dump_xml(xml, i_export_dir)
        o_xml = xml

        return o_xml