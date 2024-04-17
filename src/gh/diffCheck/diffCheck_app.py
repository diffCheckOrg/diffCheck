#! python3

import Rhino
import Rhino.Geometry as rg

import os
import typing

import diffCheck
import diffCheck.df_geometries

print(diffCheck.__version__)


if __name__ == "__main__":
    """
        Main function to test the package
        :param i_breps: list of breps
        :param i_export_dir: directory to export the xml
        :param i_dump: whether to dump the xml
    """
    # o_joints = diffCheck.df_joint_detector.JointDetector(i_breps[0]).run()
    # beams
    beams = []
    for brep in i_breps:
        beam = diffCheck.df_geometries.DFBeam.from_brep(brep)
        beams.append(beam)

    # assembly
    assembly1 = diffCheck.df_geometries.DFAssembly(beams, i_assembly_name)

    # dump the xml
    xml: str = assembly1.to_xml()
    if i_dump:
        assembly1.dump_xml(xml, i_export_dir)
    o_xml = xml

    # show the joint/side faces
    o_joints = [jf.to_brep() for jf in assembly1.all_joint_faces]
    o_sides = [sf.to_brep() for sf in assembly1.all_side_faces]
