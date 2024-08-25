# #! python3

# import System

# import Rhino
# import Rhino.Geometry as rg

# from ghpythonlib.componentbase import executingcomponent as component

# import diffCheck
# from diffCheck.df_geometries import DFBeam, DFAssembly
# import diffCheck.diffcheck_bindings
# import diffCheck.df_util

# import numpy as np


# class DFRemoveBeam(component):
#     def __init__(self):
#         super(DFRemoveBeam, self).__init__()
#         self._dfassembly = None

#     def RunScript(self,
#             i_assembly):

#         self._dfassembly = i_assembly
#         o_assembly = i_assembly.beams

#         beam = self._dfassembly.beams[0]
#         brep = rg.Brep()
#         for face in beam.faces:
#             brep.Append(face.to_brep_face().ToBrep())
#         brep.Compact()
#         ctr = brep.GetBoundingBox(True).Center

#         return ctr

#     # Preview overrides
#     def DrawViewportWires(self, args):
#         # args.Display.Draw2dText("X", System.Drawing.Color.FromArgb(200, 50, 150 , 255),rg.Point3d(0, 0, 0),True, 16, "Verdana")
#         for beam in self._dfassembly.beams:


#             df_cloud = diffCheck.diffcheck_bindings.dfb_geometry.DFPointCloud()
#             df_cloud.points = [np.array([vertex.Location.X, vertex.Location.Y, vertex.Location.Z]).reshape(3, 1) for vertex in beam.to_brep().Vertices]
#             obb: rg.Brep = diffCheck.df_cvt_bindings.cvt_dfOBB_2_rhbrep(df_cloud.get_tight_bounding_box())
#             # args.Display.DrawBrepWires(obb, System.Drawing.Color.Red, -1)

#             # get the two smallest faces of the obb
#             obb_faces = obb.Faces
#             obb_faces = sorted(obb_faces, key=lambda face: rg.AreaMassProperties.Compute(face).Area)
#             obb_endfaces = obb_faces[:2]
#             beam_axis = rg.Line(obb_endfaces[0].GetBoundingBox(True).Center, obb_endfaces[1].GetBoundingBox(True).Center)
#             extension_length = 0.5 * diffCheck.df_util.get_doc_2_meters_unitf()
#             beam_axis.Extend(extension_length, extension_length)
#             args.Display.DrawArrow(beam_axis, System.Drawing.Color.Magenta)

#             #draw the beam index
#             anchor_pt: rg.Point3d = beam_axis.From - beam_axis.UnitTangent * 0.5 * extension_length
#             args.Display.Draw2dText(
#                 str(beam.index_assembly),
#                 System.Drawing.Color.Violet,
#                 anchor_pt,
#                 True, 18)


#     # def DrawViewportMeshes(self, args):
#     #     # draw a box
#     #     for beam in self._dfassembly.beams:
#     #         df_cloud = diffCheck.diffcheck_bindings.dfb_geometry.DFPointCloud()
#     #         df_cloud.points = [np.array([vertex.Location.X, vertex.Location.Y, vertex.Location.Z]).reshape(3, 1) for vertex in beam.to_brep().Vertices]
#     #         obb = diffCheck.df_cvt_bindings.cvt_dfOBB_2_rhbrep(df_cloud.get_tight_bounding_box())

#     #         box = Rhino.Geometry.Box(obb.plane, obb.x_axis, obb.y_axis, obb.z_axis, obb.x_size, obb.y_size, obb.z_size)
#     #         args.Display.DrawBox(box, System.Drawing.Color.Red)

# # if __name__ == "__main__":
# #     comp = DFRemoveBeam()
# #     o_assembly = comp.RunScript(
# #         i_assembly
# #     )
