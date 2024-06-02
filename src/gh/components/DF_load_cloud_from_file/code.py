#! python3

import System

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
from diffCheck import diffcheck_bindings
import diffCheck.df_cvt_bindings

class DFLoadCloudFromFile(component):
    def RunScript(self,
        i_path: str,
        i_scalef: float) -> rg.PointCloud:
        """
            Import a cloud from a file and scale it if needed.

            :param i_path: path to the file
            :param i_scalef: scale factor

            :return o_out: rhino cloud
        """
        # import and convert to rhino cloud
        df_cloud = diffcheck_bindings.dfb_geometry.DFPointCloud()
        df_cloud.load_from_PLY(i_path)
        rh_cloud = diffCheck.df_cvt_bindings.cvt_dfcloud_2_rhcloud(df_cloud)

        # scale  if needed
        centroid = rh_cloud.GetBoundingBox(True).Center
        x_form_scale = rg.Transform.Scale(centroid, i_scalef)
        rh_cloud.Transform(x_form_scale)

        return [rh_cloud]  # do this to output  'Rhino.Geometry.PointCloud' instead of 'Rhino.Geometry.PointCloudItem'