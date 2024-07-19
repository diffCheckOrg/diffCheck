#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings
from diffCheck import df_vizualization


class Vizualization(component):
    def RunScript(self,
        i_results,
        i_viz_settings):
        """
            sth sth
        """

       

        distances_flattened = [item for sublist in i_results.distances for item in sublist]

        if i_viz_settings.lower_threshold is not None:
            min_value = i_viz_settings.lower_threshold
        else:
            # filter min,max value based on type
            if i_viz_settings.valueType == "Dist":
                min_value = min(min(sublist) for sublist in i_results.distances)
            elif i_viz_settings.valueType == "MSE":
                min_value = min(i_results.distances_mse)

        if i_viz_settings.upper_threshold is not None:
            max_value = i_viz_settings.upper_threshold
        else:
            if i_viz_settings.valueType == "Dist":
                max_value = max(max(sublist) for sublist in i_results.distances)
            elif i_viz_settings.valueType == "MSE":
                max_value = max(i_results.distances_mse)

        # check if i_results.source is a list of pointclouds or a mesh
        if type(i_results.source[0]) is diffcheck_bindings.dfb_geometry.DFPointCloud:

            # convert to Rhino PCD
            o_source = [df_cvt_bindings.cvt_dfcloud_2_rhcloud(src) for src in i_results.source]


            # color geometry
            if i_viz_settings.valueType == "Dist":
                o_colored_geo = [df_vizualization.color_pcd(src, dist, min_value, max_value, i_viz_settings) for src, dist in zip(o_source, i_results.distances)]
            elif i_viz_settings.valueType == "MSE":
                o_colored_geo = [df_vizualization.color_pcd(src, [dist], min_value, max_value, i_viz_settings) for src, dist in zip(o_source, i_results.distances_mse)]

        elif type(i_results.source[0]) is rg.Mesh:
            # convert to Rhino Mesh
            o_source = i_results.source

            # color geometry
            if i_viz_settings.valueType == "Dist":
                o_colored_geo = [df_vizualization.color_mesh(src, dist, min_value, max_value, i_viz_settings) for src, dist in zip(o_source, i_results.distances)]
            elif i_viz_settings.valueType == "MSE":
                o_colored_geo = [df_vizualization.color_mesh(src, [dist], min_value, max_value, i_viz_settings) for src, dist in zip(o_source, i_results.distances_mse)]

        o_legend = df_vizualization.create_legend(min_value, max_value, i_viz_settings)

        o_histogram = df_vizualization.create_histogram(distances_flattened, min_value, max_value)

        return o_source, o_colored_geo, o_legend, o_histogram


if __name__ == "__main__":
    com = Vizualization()
    o_source, o_colored_geo, o_legend, o_histogram  = com.RunScript(
        i_results,
        i_viz_settings
        )