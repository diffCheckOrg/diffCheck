#! python3

import Rhino
import Rhino.Geometry as rg

import os
import typing

import diffCheck

# import diffCheck.df_joint_detector  # diffCheck.
import diffCheck.df_geometries  # diffCheck.
# # from diffCheck.df_geometries import DFVertex, DFFace, DFBeam, DFAssembly  # diffCheck.
# # import diffCheck.df_transformations  # diffCheck.
# # import diffCheck.df_util  # diffCheck.


if __name__ == "__main__":
    joint_detector = diffCheck.df_joint_detector.JointDetector(brep=i_breps[0]).run()
    print(type(joint_detector))
    # print(joint_detector.run())
    beam = diffCheck.df_geometries.DFBeam.from_brep(i_breps[0])
    """
    Main function to test the package
    :param i_breps: list of breps
    :param i_export_dir: directory to export the xml
    :param i_dump: whether to dump the xml
    """
    # beams
    beams : typing.List[diffCheck.df_geometries.DFBeam] = []
    for brep in i_breps:
        beam = diffCheck.df_geometries.DFBeam.from_brep(brep)
        beams.append(beam)

    # assembly
    assembly1 = diffCheck.df_geometries.DFAssembly(beams, i_assembly_name)

    # dump the xml
    xml : str = assembly1.to_xml()
    if i_dump:
        assembly1.dump_xml(xml, i_export_dir)
    o_xml = xml

    # show the joint/side faces
    o_joints = [jf.to_brep() for jf in assembly1.all_joint_faces]
    o_sides = [sf.to_brep() for sf in assembly1.all_side_faces]