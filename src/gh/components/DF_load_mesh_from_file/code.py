#! python3

import System

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
from diffCheck import diffcheck_bindings
import diffCheck.df_geometries
import diffCheck.df_cvt_bindings


class DFLoadMeshFromFile(component):
    def RunScript(self,
        i_path : str,
        i_scalef : float
    ) -> rg.PointCloud:
        """
            This compoonent load a mesh rhino from a ply file.

            :param i_path: path to the ply file
            :param i_scalef: scale factor

            :return o_mesh: rhino mesh
        """
        print(f"diffCheck version: {diffCheck.__version__}")

        df_cloud = diffcheck_bindings.dfb_geometry.DFPointCloud()
        df_cloud.load_from_PLY(i_path)
        rgpoints = [rg.Point3d(pt[0], pt[1], pt[2]) for pt in df_cloud.points]
        rh_cloud = rg.PointCloud(rgpoints)

        # scale  if needed
        centroid = rh_cloud.GetBoundingBox(True).Center
        x_form_scale = rg.Transform.Scale(centroid, i_scalef)
        rh_cloud.Transform(x_form_scale)


        rh_mesh = rh_cloud

        return rh_mesh


# if __name__ == "__main__":
#     com = DFLoadMeshFromFile()
#     o_rh_mesh = com.RunScript(
#         i_path,n
#         i_scalef
#     )