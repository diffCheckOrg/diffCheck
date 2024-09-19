#! python3

import System

import typing

import Rhino.Geometry as rg

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
from diffCheck.df_geometries import DFAssembly
import diffCheck.diffcheck_bindings
import diffCheck.df_util

import numpy as np


def add_bool_toggle(self,
    nickname: str,
    indx: int,
    X_param_coord: float,
    Y_param_coord: float,
    X_offset: int=87
    ) -> None:
    """
        Adds a boolean toggle to the component input

        :param nickname: the nickname of the value list
        :param indx: the index of the input parameter
        :param X_param_coord: the x coordinate of the input parameter
        :param Y_param_coord: the y coordinate of the input parameter
        :param X_offset: the offset of the value list from the input parameter
    """
    param = ghenv.Component.Params.Input[indx]  # noqa: F821
    if param.SourceCount == 0:
        toggle = gh.Kernel.Special.GH_BooleanToggle()
        toggle.NickName = nickname
        toggle.Description = "Toggle the value to use with DFVizSettings"
        toggle.CreateAttributes()
        toggle.Attributes.Pivot = System.Drawing.PointF(
            X_param_coord - (toggle.Attributes.Bounds.Width) - X_offset,
            Y_param_coord - (toggle.Attributes.Bounds.Height / 2 + 0.1)
            )
        toggle.Attributes.ExpireLayout()
        gh.Instances.ActiveCanvas.Document.AddObject(toggle, False)
        ghenv.Component.Params.Input[indx].AddSource(toggle)  # noqa: F821

class DFPreviewAssembly(component):
    def __init__(self):
        super(DFPreviewAssembly, self).__init__()
        self._dfassembly = None
        self._joint_rnd_clr = None

        ghenv.Component.ExpireSolution(True)  # noqa: F821
        ghenv.Component.Attributes.PerformLayout()  # noqa: F821
        params = getattr(ghenv.Component.Params, "Input")  # noqa: F821
        for j in range(len(params)):
            Y_cord = params[j].Attributes.InputGrip.Y + 1
            X_cord = params[j].Attributes.Pivot.X + 20
            input_indx = j
            if "i_are_joints_visible" == params[j].NickName:
                add_bool_toggle(
                    ghenv.Component,  # noqa: F821
                    "show_joints",
                    input_indx, X_cord, Y_cord)


    def RunScript(self,
        i_assembly: DFAssembly=None,
        i_are_joints_visible: bool=None
        ):
        if i_assembly is None:
            return None
        if i_are_joints_visible is None:
            i_are_joints_visible = False

        self._dfassembly = i_assembly

        self._joint_rnd_clr = [System.Drawing.Color.FromArgb(
            System.Convert.ToInt32(255 * np.random.rand()),
            System.Convert.ToInt32(255 * np.random.rand()),
            System.Convert.ToInt32(255 * np.random.rand())) for _ in range(len(self._dfassembly.beams))]

        self._are_joints_visible = i_are_joints_visible

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
            if self._are_joints_visible:
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

                        ghenv.Component.AddRuntimeMessage(RML.Remark, "legend joint naming: the beam index - the joint index - the face index by list order")  # noqa: F821
                        name_face_joint: str = f"{beam.index_assembly}-{joint.id}-{idx_face}"
                        args.Display.Draw2dText(
                            name_face_joint,
                            self._joint_rnd_clr[idx_joint],
                            ln.To,
                            True, 18)
