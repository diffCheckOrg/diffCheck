#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
import scriptcontext as sc

from ghpythonlib.componentbase import executingcomponent as component

import diffCheck
from diffCheck.df_geometries import DFBeam, DFAssembly


class DFBuildAssembly(component):
    def RunScript(self,
            i_assembly_name,
            i_breps : System.Collections.Generic.IList[Rhino.Geometry.Brep]):
        beams: typing.List[DFBeam] = []
        for brep in i_breps:
            beam = DFBeam.from_brep_face(brep)
            beams.append(beam)

        o_assembly = DFAssembly(beams, i_assembly_name)

        return o_assembly