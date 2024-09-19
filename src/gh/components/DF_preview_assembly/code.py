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

    def RunScript(self, i_assembly: DFAssembly=None):
        if i_assembly is None:
            return None

        self._dfassembly = i_assembly

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
            args.Display.DrawBrepWires(obb, System.Drawing.Color.Red)

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
