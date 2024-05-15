#! python3

import System

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings

class DFLoadMeshFromFile(component):
    def RunScript(self,
        i_path: str,
        i_scalef: float) -> rg.Mesh:
        """
            This compoonent loads a Rhino mesh from a .ply file.

            :param i_path: path to the .ply file
            :param i_scalef: scale factor

            :return o_mesh: Rhino Mesh
        """
        # import and convert to Rhino Mesh
        df_mesh = diffcheck_bindings.dfb_geometry.DFMesh()
        df_mesh.load_from_PLY(i_path)
        rh_mesh = df_cvt_bindings.cvt_dfmesh_2_rhmesh(df_mesh)

        # scale  if needed
        centroid = rh_mesh.GetBoundingBox(True).Center
        x_form_scale = rg.Transform.Scale(centroid, i_scalef)
        rh_mesh.Transform(x_form_scale)

        return [rh_mesh]

if __name__ == "__main__":
    com = DFLoadMeshFromFile()
    o_rh_mesh = com.RunScript(i_path, i_scalef)