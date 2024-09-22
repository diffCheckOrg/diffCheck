#! python3

import System

from ghpythonlib.componentbase import executingcomponent as component


class DFDeconstructBeam(component):
    def RunScript(self, i_beams: System.Collections.Generic.List[object]):
        o_side_faces, o_joint_faces, o_joint_ids = [], [], []

        for i_b in i_beams:
            o_side_faces = [f.to_brep_face() for f in i_b.side_faces]
            o_joint_faces = [f.to_brep_face() for f in i_b.joint_faces]
            o_joint_ids = [f.joint_id for f in i_b.joint_faces]

        return o_side_faces, o_joint_faces, o_joint_ids
