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
        Adds color to the mesh or point cloud and generates a corresponding legend and histogram
        """

        values, min_value, max_value = df_vizualization.filter_values_based_on_valuetype(i_results, i_viz_settings)

        # check if i_results.source is a list of pointclouds or a mesh
        if type(i_results.source[0]) is diffcheck_bindings.dfb_geometry.DFPointCloud:

            # convert to Rhino PCD
            o_source = [df_cvt_bindings.cvt_dfcloud_2_rhcloud(src) for src in i_results.source]

            # color geometry
            o_colored_geo = [df_vizualization.color_pcd(src, dist, min_value, max_value, i_viz_settings) for src, dist in zip(o_source, values)]


        elif type(i_results.source[0]) is rg.Mesh:
            # convert to Rhino Mesh
            o_source = i_results.source

            # color geometry
            o_colored_geo = [df_vizualization.color_mesh(src, dist, min_value, max_value, i_viz_settings) for src, dist in zip(o_source, values)]

        o_legend = df_vizualization.create_legend(min_value, max_value, i_viz_settings)

        o_histogram = df_vizualization.create_histogram(values, min_value, max_value)

        return o_source, o_colored_geo, o_legend, o_histogram


if __name__ == "__main__":
    com = Vizualization()
    o_source, o_colored_geo, o_legend, o_histogram  = com.RunScript(
        i_results,
        i_viz_settings
        )