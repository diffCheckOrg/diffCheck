#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings
from diffCheck import df_error_estimation, df_vizualization

import diffCheck.df_util


class Vizualization(component):
    def RunScript(self,
        i_results,
        i_viz_settings):
        """
            sth sth
        """

        if i_results.source is None or i_results.target is None:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Please provide both objects of type point clouds to compare")
            return None

        # check if target is a pcl
        o_source = [df_cvt_bindings.cvt_dfcloud_2_rhcloud(src) for src in i_results.source]

        # by default we color the target
        min_value = min(min(sublist) for sublist in i_results.distances)
        max_value = max(max(sublist) for sublist in i_results.distances)
        
        o_source = [df_vizualization.add_color(src, dist, min_value, max_value) for src, dist in zip(o_source, i_results.distances)]

        o_target = [df_cvt_bindings.cvt_dfcloud_2_rhcloud(trg) for trg in i_results.target]

        o_legend = []

        # color the source pointcloud based on viz_settings

         #make a legend

        return o_source, o_target, o_legend


if __name__ == "__main__":
    com = Vizualization()
    o_source, o_target, o_legend,  = com.RunScript(
        i_results,
        i_viz_settings
        )