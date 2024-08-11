#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
import scriptcontext as sc

from ghpythonlib.componentbase import executingcomponent as component

import diffCheck
from diffCheck.df_geometries import DFBeam, DFAssembly


class DFDeconstructBeam(component):
    def RunScript(self,
            i_beams : typing.List[DFBeam]):
        o_side_faces, o_joint_faces, o_joint_ids, o_breps = [], [], [], []

        for i_b in i_beams:
            o_side_faces = [f.to_brep_face() for f in i_b.side_faces]
            o_joint_faces = [f.to_brep_face() for f in i_b.joint_faces]
            o_joint_ids = [f.joint_id for f in i_b.joint_faces]

        return o_side_faces, o_joint_faces, o_joint_ids
