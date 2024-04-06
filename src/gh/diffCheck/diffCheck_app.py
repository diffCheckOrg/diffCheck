#! python3
"""
    This module is used as entry point to test the package in Rh/Gh
"""

import Rhino
import Rhino.Geometry as rg

import os
from df_geometries import DFVertex, DFFace, DFBeam, DFAssembly  # diffCheck.df_geometries 

def main():
    # vertices
    vertex1 = DFVertex(1, 2, 3)
    vertex2 = DFVertex(4, 5, 6)
    vertex3 = DFVertex(7, 8, 9)
    vertex4 = DFVertex(10, 11, 12)
    vertex5 = DFVertex(13, 14, 15)
    # print(vertex1.x)
    # print(vertex2.y)
    # print(vertex3.z)

    # faces
    face1 = DFFace([vertex1, vertex2, vertex3], 1)
    face2 = DFFace([vertex4, vertex5, vertex3, vertex4], 2)
    face3 = DFFace([vertex1, vertex2, vertex5], 3)
    face4 = DFFace([vertex1, vertex2, vertex3, vertex4])
    face5 = DFFace([vertex1, vertex2, vertex3, vertex4, vertex5])
    face6 = DFFace([vertex1, vertex2, vertex3, vertex4, vertex5, vertex1])
    # print(face1.id)
    # print(face2.is_joint)
    # print(face3.is_joint)

    # beams
    beam1 = DFBeam("Beam1", [face1, face2, face3, face4])
    beam2 = DFBeam("Beam2", [face1, face2, face3, face4, face5, face6])
    beam3 = DFBeam.from_brep(brep)
    print(beam3)
    # print(beam1.id)
    # print(beam2.id)

    # assembly
    assembly = DFAssembly([beam1, beam2], "Assembly1")
    print(assembly.beams)
    print(assembly)

if __name__ == "__main__":
    main()