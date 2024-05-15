#! python3

import System

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings

class DFLoadCloudFromFile(component):
    def RunScript(self,
        i_path: str,
        i_scalef: float) -> rg.PointCloud:
        """
            This component loads a point cloud from a .ply file.

            :param i_path: path to the .ply file
            :param i_scalef: scale factor

            :return o_rh_cloud: Rhino PointCloud
        """
        # import and convert to Rhino Cloud
        df_cloud = diffcheck_bindings.dfb_geometry.DFPointCloud()
        df_cloud.load_from_PLY(i_path)
        rh_cloud = df_cvt_bindings.cvt_dfcloud_2_rhcloud(df_cloud)

        # scale  if needed
        centroid = rh_cloud.GetBoundingBox(True).Center
        x_form_scale = rg.Transform.Scale(centroid, i_scalef)
        rh_cloud.Transform(x_form_scale)
        
        return [rh_cloud]
    
# if __name__ == "__main__":
#     com = DFLoadCloudFromFile()
#     o_rh_cloud = com.RunScript(i_path, i_scalef)