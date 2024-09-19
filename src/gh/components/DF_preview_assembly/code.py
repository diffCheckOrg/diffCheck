#! python3

import System

import typing

import Rhino.Geometry as rg

from ghpythonlib.componentbase import executingcomponent as component

import diffCheck
from diffCheck.df_geometries import DFAssembly
import diffCheck.diffcheck_bindings
import diffCheck.df_util

import numpy as np


class DFPreviewAssembly(component):
    def __init__(self):
        super(DFPreviewAssembly, self).__init__()
        self._dfassembly = None
        self._joint_rnd_clr = None

    def RunScript(self, i_assembly: DFAssembly=None):
        if i_assembly is None:
            return None

        self._dfassembly = i_assembly

        self._joint_rnd_clr = [System.Drawing.Color.FromArgb(
            System.Convert.ToInt32(255 * np.random.rand()),
            System.Convert.ToInt32(255 * np.random.rand()),
            System.Convert.ToInt32(255 * np.random.rand())) for _ in range(len(self._dfassembly.beams))]
        return None

    # Preview overrides
    def DrawViewportWires(self, args):
        for beam in self._dfassembly.beams:
            #######################################
            ## DFBeams
            #######################################
            # beams' obb
            df_cloud = diffCheck.diffcheck_bindings.dfb_geometry.DFPointCloud()
            vertices_pt3d_rh : typing.List[rg.Point3d] = [vertex.to_rg_point3d() for vertex in beam.vertices]
            df_cloud.points = [np.array([vertex.X, vertex.Y, vertex.Z]).reshape(3, 1) for vertex in vertices_pt3d_rh]
            obb: rg.Brep = diffCheck.df_cvt_bindings.cvt_dfOBB_2_rhbrep(df_cloud.get_tight_bounding_box())
            # args.Display.DrawBrepWires(obb, System.Drawing.Color.Red)  ## keep for debugging

            # axis arrow
            obb_faces = obb.Faces
            obb_faces = sorted(obb_faces, key=lambda face: rg.AreaMassProperties.Compute(face).Area)
            obb_endfaces = obb_faces[:2]
            beam_axis = rg.Line(obb_endfaces[0].GetBoundingBox(True).Center, obb_endfaces[1].GetBoundingBox(True).Center)
            extension_length = 0.5 * diffCheck.df_util.get_doc_2_meters_unitf()
            beam_axis.Extend(extension_length, extension_length)
            args.Display.DrawArrow(beam_axis, System.Drawing.Color.Magenta)

            # beam assembly index
            anchor_pt: rg.Point3d = beam_axis.From - beam_axis.UnitTangent * 0.5 * extension_length
            args.Display.Draw2dText(
                str(beam.index_assembly),
                System.Drawing.Color.Violet,
                anchor_pt,
                True, 18)

            #######################################
            ## DFJoints
            #######################################
            # draw an hatch for each joint's face
            # beam_center = beam.center
            # beam_idx
            for idx_joint, joint in enumerate(beam.joints):
                joint_faces = joint.faces
                for idx_face, face in enumerate(joint_faces):
                    face_center = face.to_brep_face().GetBoundingBox(False).Center
                    args.Display.DrawPoint(face_center, self._joint_rnd_clr[idx_joint])

                    vector_face_center_2_beam_center = face_center - beam.center
                    vector_face_center_2_beam_center.Unitize()
                    vector_face_center_2_beam_center *= 0.4 * extension_length

                    ln = rg.Line(face_center, face_center + vector_face_center_2_beam_center)
                    args.Display.DrawDottedLine(ln, self._joint_rnd_clr[idx_joint])

                    # name of the joint is defined by: 1) the beam index, 2) the joint index, 3) the face index
                    name_face_joint: str = f"{beam.index_assembly}-{idx_joint}-{idx_face}"
                    args.Display.Draw2dText(
                        name_face_joint,
                        self._joint_rnd_clr[idx_joint],
                        ln.To,
                        True, 18)
                # joint_faces = joint.faces
                # for face in joint_faces:
                #     mesh_rh = face.to_mesh()

                #     args.Display.DrawMeshWires(mesh_rh, System.Drawing.Color.Blue)
