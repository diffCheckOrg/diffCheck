#! python3

import diffCheck
from diffCheck.df_geometries import DFBeam, DFAssembly

from ghpythonlib.componentbase import executingcomponent as component

import System

class DFMergeAssemblies(component):
    def RunScript(self,
                  i_new_name: str,
                  i_assemblies: System.Collections.Generic.IList[diffCheck.df_geometries.DFAssembly]
                  ) -> diffCheck.df_geometries.DFAssembly:

        beams = System.Collections.Generic.List[DFBeam]()
        for assembly in i_assemblies:
            for beam in assembly.beams:
                beams.Add(beam)

        o_assembly = DFAssembly(beams, i_new_name)

        return o_assembly
