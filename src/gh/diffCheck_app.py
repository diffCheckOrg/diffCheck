#! python3
"""
    This module is used as entry point to test the package in Rh/Gh
"""

import os
from diffCheck.geometries import Beam, Assembly

def main():
    beam1 = Beam("Beam1", True)
    beam2 = Beam("Beam2", False)
    print(beam1.id)
    print(beam2.id)
    
    assembly = Assembly([beam1, beam2], "Assembly1")
    print(assembly.beams)
    print(assembly.name)

if __name__ == "__main__":
    main()