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

        # TODO: test
        o_debug = []

        # mass_ctrs = []
        # crt_brep = i_breps[5]
        breps_repaired = []
        for brep in i_breps:

            # convert mesh to brep object
            mesh=Rhino.Geometry.Mesh()
            mesh_parts=Rhino.Geometry.Mesh.CreateFromBrep(
                brep,
                Rhino.Geometry.MeshingParameters.Coarse)
            for mesh_part in mesh_parts: mesh.Append(mesh_part)
            mesh.Compact()
            mesh.MergeAllCoplanarFaces(Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance, True)
            # o_debug.append(mesh)

            # get the obb
            df_mesh = diffCheck.df_cvt_bindings.cvt_rhmesh_2_dfmesh(mesh)
            df_cloud = df_mesh.sample_points_uniformly(200)
            df_OBB = df_cloud.get_tight_bounding_box()
            rh_OBB = diffCheck.df_cvt_bindings.cvt_dfOBB_2_rhbrep(df_OBB)

            # check if the OBB is closed
            # print(f"OBB is closed: {rh_OBB.IsSolid}")  # FIXME: brep is not closed
            # o_debug.append(rh_OBB)

            # get OBB_center
            rh_OBB_center = rh_OBB.GetBoundingBox(True).Center
            # o_debug.append(rh_OBB_center)

            # local axis system get the longest/shortes edge of the rh_OBB with a lambda function
            edges = rh_OBB.Edges
            edge_lengths = [edge.GetLength() for edge in edges]
            longest_edge = edges[edge_lengths.index(max(edge_lengths))]
            shortest_edge = edges[edge_lengths.index(min(edge_lengths))]

            # scale the box in the longest edge direction by 1.5 from center on both directions
            rh_OBB_zaxis = rg.Vector3d(longest_edge.PointAt(1) - longest_edge.PointAt(0))
            rh_OBB_plane = rg.Plane(rh_OBB_center, rh_OBB_zaxis)
            scale_factor = 0.09
            xform = rg.Transform.Scale(
                rh_OBB_plane,
                1-scale_factor,
                1-scale_factor,
                1+scale_factor
            )
            rh_OBB.Transform(xform)

            # get all the centers of the faces
            # face_centers = []
            faces = {}
            for idx, face in enumerate(brep.Faces):
                face_center = rg.AreaMassProperties.Compute(face).Centroid
                if rh_OBB.IsPointInside(face_center, sc.doc.ModelAbsoluteTolerance, True):
                    # face_centers.append(face_center)
                    faces[idx] = (face, True)
                    # o_debug.append(brep.Faces[idx])
                else:
                    faces[idx] = (face, False)
                    # o_debug.append(brep.Faces[idx])

            face_jointid = {}  # face : joint id (int)
            joint_counter = 0
            for key, value in faces.items():
                # print(f"Face {key} is inside: {value[1]}")
                if value[1]:
                    face_jointid[key] = joint_counter
                    adjacent_faces = value[0].AdjacentFaces()
                    for adj_face in adjacent_faces:
                        if faces[adj_face][1]:
                            face_jointid[value] = joint_counter
                    joint_counter += 1
                else:
                    face_jointid[value] = None

            o_sides = [faces[key][0] for key, value in faces.items() if not value[1]]
            o_joints = [faces[key][0] for key, value in faces.items() if value[1]]




            # get the faces that are t


        ########################################

        # for f in crt_brep.Faces:
        #     mass_ctr = rg.AreaMassProperties.Compute(f).Centroid
        #     is_inside : bool = aabb.Contains(mass_ctr, strict=True)
        #     print(f"Face {f} is inside: {is_inside}")
        #     if is_inside:
        #         mass_ctrs.append(mass_ctr)
        # o_debug = mass_ctrs

        # # beams
        # beams: typing.List[DFBeam] = []
        # for brep in i_breps:
        #     beam = DFBeam.from_brep(brep)
        #     beams.append(beam)

        # # assembly
        # assembly1 = DFAssembly(beams, i_assembly_name)

        # # dump the xml
        # xml: str = assembly1.to_xml()
        # if i_dump:
        #     assembly1.dump_xml(xml, i_export_dir)
        # o_xml = xml

        # # show the joint/side faces
        # o_joints = [jf.to_brep() for jf in assembly1.all_joint_faces]
        # o_sides = [sf.to_brep() for sf in assembly1.all_side_faces]

        return o_xml, o_joints, o_sides, o_debug


if __name__ == "__main__":
    com = DFXMLExporter()
    o_xml, o_joints, o_sides, o_debug = com.RunScript(
        i_dump,
        i_assembly_name,
        i_export_dir,
        i_breps
    )