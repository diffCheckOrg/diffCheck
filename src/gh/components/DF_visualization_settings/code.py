#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

from diffCheck import df_visualization

class DFVisualizationSettings(component):
    def RunScript(self,
        i_value_type: str,
        i_upper_threshold: float,
        i_lower_threshold: float,
        i_palette: str,
        i_legend_height: float,
        i_legend_width: float,
        i_legend_plane: rg.Plane,
        i_histogram_scale_factor: float):
        if i_palette not in  ["Jet", "Rainbow", "RdPu", "Viridis"]:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Possible values for i_palette are: Jet, Rainbow, RdPu, Viridis")
            return None
        
        if i_value_type not in  ["Dist", "RMSE", "MAX", "MIN", "STD"]:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Possible values for i_value_type are: dist, RMSE, MAX, MIN, STD")
            return None
        
        # set default values
        if i_legend_height is None: i_legend_height = 10
        if i_legend_width is None: i_legend_width = 0.5
        if i_legend_plane is None: i_legend_plane = rg.Plane.WorldXY
        if i_histogram_scale_factor is None: i_histogram_scale_factor = 0.01

        # pack settings
        o_viz_settings = df_visualization.DFVizSettings(i_value_type,
                                                        i_upper_threshold,
                                                        i_lower_threshold,
                                                        i_palette,
                                                        i_legend_height,
                                                        i_legend_width,
                                                        i_legend_plane,
                                                        i_histogram_scale_factor)

        return o_viz_settings