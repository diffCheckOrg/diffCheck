#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
from diffCheck import df_vizualization

import diffCheck.df_util


class VisualizationSettings(component):
    def RunScript(self,
        i_source_value_type,
        i_target_value_type,
        i_upper_threshold,
        i_lower_threshold,
        i_palette):
        """
            sth
        """

        # pack settings
        o_viz_settings = df_vizualization.DFVizSettings(i_source_value_type, i_target_value_type, i_upper_threshold, i_lower_threshold, i_palette)

        return o_viz_settings

if __name__ == "__main__":
    com = VisualizationSettings()
    o_viz_settings = com.RunScript(
        i_source_value_type,
        i_target_value_type,
        i_upper_threshold,
        i_lower_threshold,
        i_palette
        )