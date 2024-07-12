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
from diffCheck import df_error_estimation

import diffCheck.df_util


class Vizualization(component):
    def RunScript(self,
        i_results,
        i_target_flag,
        i_source_flag,
        i_viz_settings):
        """
            sth sth
        """

        if i_results.source is None or i_results.target is None:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Please provide both objects of type point clouds to compare")
            return None

        if i_target_flag == False:
            #if user doesn't want to vizualize results on the target return the original geo
            #now only implemented for PCD
            o_target = df_cvt_bindings.cvt_dfcloud_2_rhcloud(i_results.target)
            o_target_legend = []
        else:
            #color the target pointcloud based on viz_settings

            #make a legend

            pass

        if i_source_flag == False:
            #if user doesn't want to vizualize results on the target return the original geo
            #now only implemented for PCD
            o_source = df_cvt_bindings.cvt_dfcloud_2_rhcloud(i_results.source)
            o_source_legend = []
        else:
            #color the source pointcloud based on viz_settings

            #make a legend

            pass

        return o_source, o_target, o_source_legend, o_target_legend


if __name__ == "__main__":
    com = Vizualization()
    o_source, o_target, o_source_legend, o_target_legend = com.RunScript(
        i_results,
        i_target_flag,
        i_source_flag,
        i_viz_settings
        )