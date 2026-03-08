#! python3

import System
import typing

import Rhino

from ghpythonlib.componentbase import executingcomponent as component

from diffCheck.df_geometries import DFBeam, DFAssembly


class DFBuildAssembly(component):
    def RunScript(self,
            i_assembly_name,
            i_breps : System.Collections.Generic.IList[Rhino.Geometry.Brep],
            i_is_roundwood : bool,
            i_allow_curved_joint_faces : bool):
        beams: typing.List[DFBeam] = []

        if i_assembly_name is None or i_breps is None:
            return None

        if i_is_roundwood is None:
            i_is_roundwood = False

        if i_allow_curved_joint_faces is None:
            i_allow_curved_joint_faces = False

        for brep in i_breps:
            beam = DFBeam.from_brep_face(brep, i_is_roundwood, i_allow_curved_joint_faces)
            beams.append(beam)

        o_assembly = DFAssembly(beams, i_assembly_name)

        return o_assembly
