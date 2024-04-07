#! python3
"""
    This module is used as entry point to test the package in Rh/Gh
"""

import Rhino
import Rhino.Geometry as rg

import os
import typing

from df_geometries import DFBeam, DFAssembly  # diffCheck.df_geometries 


def main(
    i_breps : typing.List[rg.Brep],
    i_export_dir : str
    ):
    """
    Main function to test the package
    :param i_breps: list of breps
    :param i_export_dir: directory to export the xml
    """
    
    # beams
    beams : typing.List[DFBeam] = []
    for brep in i_breps:
        beam = DFBeam.from_brep(brep)
        beams.append(beam)

    # assembly
    assembly1 = DFAssembly(beams, "Assembly1")
    print(assembly1.beams)
    print(assembly1)

    # dump the xml
    xml : str = assembly1.dump_to_xml(i_export_dir)
    o_xml = xml

    # # (optional) you can also load the xml
    # file_path = os.path.join(i_export_dir, "Assembly1_0.xml")
    # assembly2 = DFAssembly.from_xml(file_path)

if __name__ == "__main__":
    main(i_breps,
         i_export_dir)