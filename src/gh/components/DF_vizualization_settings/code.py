#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

from diffCheck import df_vizualization

class VisualizationSettings(component):
    def RunScript(self,
        i_value_type,
        i_upper_threshold,
        i_lower_threshold,
        i_palette,
        i_legend_height,
        i_legend_width,
        i_legend_plane,
        i_histogram_scale_factor):

        """
        Compiles all the vizualization settings to feed to the vizualization component
        """

        # set default values
        if i_palette is None: i_palette = "Jet"
        if i_legend_height is None: i_legend_height = 10
        if i_legend_width is None: i_legend_width = 0.5
        if i_legend_plane is None: i_legend_plane = rg.Plane.WorldXY
        if i_histogram_scale_factor is None: i_histogram_scale_factor = 0.01

        # pack settings
        o_viz_settings = df_vizualization.DFVizSettings(i_value_type,
                                                        i_upper_threshold,
                                                        i_lower_threshold,
                                                        i_palette,
                                                        i_legend_height,
                                                        i_legend_width,
                                                        i_legend_plane,
                                                        i_histogram_scale_factor)

        return o_viz_settings

# if __name__ == "__main__":
#     com = VisualizationSettings()
#     o_viz_settings = com.RunScript(
#         i_value_type,
#         i_upper_threshold,
#         i_lower_threshold,
#         i_palette,
#         i_legend_height,
#         i_legend_width,
#         i_legend_plane,
#         i_histogram_scale_factor
#         )