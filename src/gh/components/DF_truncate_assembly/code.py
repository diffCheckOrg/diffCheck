from ghpythonlib.componentbase import executingcomponent as component

import diffCheck
import diffCheck.df_geometries

class DFTester(component):
    def RunScript(self,
                  i_assembly,
                  i_truncate_index: int):
        beams = i_assembly.beams[:i_truncate_index]
        name = i_assembly.name

        o_assembly = diffCheck.df_geometries.DFAssembly(name=name, beams=beams)
        ghenv.Component.Message = f"number of beams: {len(o_assembly.beams)}"  # noqa: F821
        return o_assembly
