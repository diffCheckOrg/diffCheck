#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
import scriptcontext as sc

from ghpythonlib.componentbase import executingcomponent as component

import diffCheck
from diffCheck.df_geometries import DFBeam, DFAssembly
import diffCheck.df_transformations

import diffCheck.diffcheck_bindings
import diffCheck.df_cvt_bindings


class DFXMLExporter(component):
    def RunScript(self,
            i_dump: bool,
            i_assembly_name,
            i_export_dir,
            i_breps: System.Collections.Generic.IList[Rhino.Geometry.Brep]):
        """
            This read breps from Rhino, converts them to DFBeams and DFAssemblies, and exports them to XML.
            
            :param i_dump: whether to dump the xml
            :param i_export_dir: directory to export the xml
            :param i_breps: list of breps
        """
        ################
        o_xml = None
        o_joints = None
        o_sides = None
        o_debug = None
        ################
        ########################################

        # # TODO: test
        # breps_repaired = []
        # for brep in i_breps:


        #     # brep vertices to cloud
        #     df_cloud = diffCheck.diffcheck_bindings.dfb_geometry.DFPointCloud()
        #     brep_vertices = []
        #     for vertex in brep.Vertices:
        #         brep_vertices.append(np.array([vertex.Location.X, vertex.Location.Y, vertex.Location.Z]).reshape(3, 1))
        #     df_cloud.points = brep_vertices

        #     df_OBB = df_cloud.get_tight_bounding_box()
        #     rh_OBB = diffCheck.df_cvt_bindings.cvt_dfOBB_2_rhbrep(df_OBB)

        #     # scale the box in the longest edge direction by 1.5 from center on both directions
        #     rh_OBB_center = rh_OBB.GetBoundingBox(True).Center
        #     edges = rh_OBB.Edges
        #     edge_lengths = [edge.GetLength() for edge in edges]
        #     longest_edge = edges[edge_lengths.index(max(edge_lengths))]
        #     shortest_edge = edges[edge_lengths.index(min(edge_lengths))]

        #     rh_OBB_zaxis = rg.Vector3d(longest_edge.PointAt(1) - longest_edge.PointAt(0))
        #     rh_OBB_plane = rg.Plane(rh_OBB_center, rh_OBB_zaxis)
        #     scale_factor = 0.09
        #     xform = rg.Transform.Scale(
        #         rh_OBB_plane,
        #         1-scale_factor,
        #         1-scale_factor,
        #         1+scale_factor
        #     )
        #     rh_OBB.Transform(xform)

        #     # check if face's centers are inside the OBB
        #     faces = {}
        #     for idx, face in enumerate(brep.Faces):
        #         face_center = rg.AreaMassProperties.Compute(face).Centroid
        #         if rh_OBB.IsPointInside(face_center, sc.doc.ModelAbsoluteTolerance, True):
        #             faces[idx] = (face, True)
        #         else:
        #             faces[idx] = (face, False)

        #     face_jointid = {}  # face : joint id (int) or None
        #     joint_counter = 0
        #     for key, value in faces.items():
        #         if value[1]:
        #             face_jointid[key] = joint_counter
        #             adjacent_faces = value[0].AdjacentFaces()
        #             for adj_face in adjacent_faces:
        #                 if faces[adj_face][1]:
        #                     face_jointid[value] = joint_counter
        #             joint_counter += 1
        #         else:
        #             face_jointid[value] = None

        #     faces_data = []
        #     for key, value in faces.items():
        #         faces_data.append((value[0], value[1]))
        #         print(faces_data)

        #     o_sides = [faces[key][0] for key, value in faces.items() if not value[1]]
        #     o_joints = [faces[key][0] for key, value in faces.items() if value[1]]




        ########################################

        # beams
        beams: typing.List[DFBeam] = []
        for brep in i_breps:
            beam = DFBeam.from_brep(brep)
            beams.append(beam)

        # assembly
        assembly1 = DFAssembly(beams, i_assembly_name)

        # dump the xml
        xml: str = assembly1.to_xml()
        if i_dump:
            assembly1.dump_xml(xml, i_export_dir)
        o_xml = xml

        # show the joint/side faces
        o_joints = [jf.to_brep() for jf in assembly1.all_joint_faces]
        o_sides = [sf.to_brep() for sf in assembly1.all_side_faces]

        return o_xml, o_joints, o_sides, o_debug


if __name__ == "__main__":
    com = DFXMLExporter()
    o_xml, o_joints, o_sides, o_debug = com.RunScript(
        i_dump,
        i_assembly_name,
        i_export_dir,
        i_breps
    )