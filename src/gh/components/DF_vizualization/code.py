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
        distances_flattened = [item for sublist in i_results.distances for item in sublist]

        if i_viz_settings.lower_threshold is not None:
            min_value = i_viz_settings.lower_threshold
        else:
            min_value = min(min(sublist) for sublist in i_results.distances)

        if i_viz_settings.upper_threshold is not None:
            max_value = i_viz_settings.upper_threshold
        else:
            max_value = max(max(sublist) for sublist in i_results.distances)

        # we always color the source
        # check if source is a pcd
        o_colored_geo = [df_vizualization.color_pcd(src, dist, min_value, max_value) for src, dist in zip(o_source, i_results.distances)]

        o_legend = df_vizualization.create_legend(min_value, max_value)
        
        o_histogram = df_vizualization.create_histogram(distances_flattened, min_value, max_value)

        return o_source, o_colored_geo, o_legend, o_histogram


if __name__ == "__main__":
    com = Vizualization()
    o_source, o_colored_geo, o_legend, o_histogram  = com.RunScript(
        i_results,
        i_viz_settings
        )