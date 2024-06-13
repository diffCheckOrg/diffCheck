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
        """
            Deconstruct the DFBeam object into Rhino objects.
            
            :param i_beams: the DFBeam objects

            :return o_side_faces: the side joints of the beam
            :return o_joint_faces: the face joints of the beam
            :return o_joint_ids: the ids for each face joint
        """
        o_side_faces, o_joint_faces, o_joint_ids, o_breps = [], [], [], []

        for i_b in i_beams:
            o_side_faces = [f.to_brep_face() for f in i_b.side_faces]
            o_joint_faces = [f.to_brep_face() for f in i_b.joint_faces]
            o_joint_ids = [f.joint_id for f in i_b.joint_faces]

        return o_side_faces, o_joint_faces, o_joint_ids

# if __name__ == "__main__":
#     comp = DFDeconstructBeam()
#     o_side_faces, o_joint_faces, o_joint_ids = comp.RunScript(
#         i_beams
#     )
