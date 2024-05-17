#! python3

import Rhino
import Rhino.Geometry as rg

if __name__ == "__main__":
    # if i_splits is a trimmed_surface type, than store in a list
    trimmed_surfaces = []
    for brep in i_splits:
        # get only the trimmed surfaces
        for ts in brep.Faces:
            # store the trimmed surfaces in a list
            trimmed_surfaces.append(ts)

    o_trimmed_surfaces = trimmed_surfaces