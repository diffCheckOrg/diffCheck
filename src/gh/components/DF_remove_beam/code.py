#! python3

import typing

from ghpythonlib.componentbase import executingcomponent as component

import diffCheck
import diffCheck.df_geometries
import diffCheck.diffcheck_bindings
import diffCheck.df_util


class DFRemoveBeam(component):
    def RunScript(self,
            i_assembly : diffCheck.df_geometries.DFAssembly=None,
            i_idx_2_remove : typing.List[int]=None):

        if i_assembly is None or i_idx_2_remove is None:
            return None

        o_assembly = i_assembly.deepcopy()
        for idx in i_idx_2_remove:
            o_assembly.remove_beam(idx)

        return o_assembly
