#! python3

import System

from ghpythonlib.componentbase import executingcomponent as component


class DFRemoveBeam(component):
    def RunScript(self,
            i_assembly,
            i_idx_2_remove: System.Collections.Generic.List[int]):

        if i_assembly is None or i_idx_2_remove is None:
            return None

        o_assembly = i_assembly.deepcopy()
        for idx in i_idx_2_remove:
            o_assembly.remove_beam(idx)

        return o_assembly
