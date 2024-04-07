#! python3
import Rhino
import Rhino.Geometry as rg

import os
import typing

from df_geometries import DFBeam, DFAssembly  # diffCheck.df_geometries 


if __name__ == "__main__":
    """
    Main function to test the package
    :param i_breps: list of breps
    :param i_export_dir: directory to export the xml
    :param i_dump: whether to dump the xml
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
    xml : str = assembly1.to_xml()
    if i_dump:
        assembly1.dump(xml, i_export_dir)
    o_xml = xml