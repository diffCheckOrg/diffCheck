#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
import scriptcontext as sc

from ghpythonlib.componentbase import executingcomponent as component

import diffCheck
from diffCheck.df_geometries import DFBeam, DFAssembly


class DFDeconstructAssembly(component):
    def RunScript(self,
            i_assembly):
        o_beams = i_assembly.beams
        return o_beams