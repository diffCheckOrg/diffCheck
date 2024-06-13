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
        """
            Deconstruct the DFAssembly into a set of df_beams objects.
            
            :param i_assembly: the DFAssembly object

            :return o_beams
        """
        o_beams = i_assembly.beams

        return o_beams


# if __name__ == "__main__":
#     comp = DFDeconstructAssembly()
#     o_beams = comp.RunScript(
#         i_assembly
#     )
