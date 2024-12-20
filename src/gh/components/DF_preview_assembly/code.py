#! python3

import System

import Rhino.Geometry as rg

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
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


    def RunScript(self, i_assembly, i_are_joints_visible: bool):
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
        if self._dfassembly is None:
            return
        for idx_beam, beam in enumerate(self._dfassembly.beams):
            #######################################
            ## DFBeams
            #######################################
            if len(self._dfassembly.beams) > 1:
                beam_axis = beam.axis
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
                clr = self._joint_rnd_clr[idx_beam]
                for idx_joint, joint in enumerate(beam.joints):
                    joint_faces = joint.faces
                    for idx_face, face in enumerate(joint_faces):
                        if len(self._dfassembly.beams) == 1:
                            clr: System.Drawing.Color = System.Drawing.Color.Magenta

                        face_center = face.to_brep_face().GetBoundingBox(False).Center
                        args.Display.DrawPoint(face_center, clr)

                        vector_face_center_2_beam_center = face_center - beam.center
                        vector_face_center_2_beam_center.Unitize()
                        vector_face_center_2_beam_center *= 0.4 * 0.5 * diffCheck.df_util.get_doc_2_meters_unitf()

                        ln = rg.Line(face_center, face_center + vector_face_center_2_beam_center)
                        args.Display.DrawDottedLine(ln, clr)

                        ghenv.Component.AddRuntimeMessage(RML.Remark, "legend joint naming: the beam index - the joint index - the face index by list order")  # noqa: F821
                        name_face_joint: str = f"{beam.index_assembly}-{joint.id}-{idx_face}"
                        args.Display.Draw2dText(
                            name_face_joint,
                            clr,
                            ln.To,
                            True, 18)
