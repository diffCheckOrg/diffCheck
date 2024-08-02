#! python3

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython

import System
import typing

import Rhino
import Rhino.Geometry as rg

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

from diffCheck import df_visualization


def add_str_valuelist(self, values_list, nickname, indx, X_param_coord, Y_param_coord, X_offset=40):
    param = ghenv.Component.Params.Input[indx]
    if param.SourceCount == 0:
        valuelist = Grasshopper.Kernel.Special.GH_ValueList()
        valuelist.NickName = nickname
        valuelist.Description = "Select the value to use with DFVizSettings"
        selected = valuelist.FirstSelectedItem
        valuelist.ListItems.Clear()
        for v in values_list:
            vli = gh.Kernel.Special.GH_ValueListItem(str(v),str('"' + v + '"'))
            valuelist.ListItems.Add(vli)
        if selected in values_list:
            valuelist.SelectItem(values_list.index(selected))
        valuelist.CreateAttributes()
        valuelist.Attributes.Pivot = System.Drawing.PointF(
            X_param_coord - (valuelist.Attributes.Bounds.Width) - X_offset,
            Y_param_coord - (valuelist.Attributes.Bounds.Height / 2 + 0.1)
            )
        valuelist.Attributes.ExpireLayout()
        Grasshopper.Instances.ActiveCanvas.Document.AddObject(valuelist, False)
        ghenv.Component.Params.Input[indx].AddSource(valuelist)

class DFVisualizationSettings(component):
    def __init__(self):
        self.poss_value_types = ["Dist", "RMSE", "MAX", "MIN", "STD"]
        self.poss_palettes = ["Jet", "Rainbow", "RdPu", "Viridis"]
        
        ghenv.Component.ExpireSolution(True)
        ghenv.Component.Attributes.PerformLayout()
        params = getattr(ghenv.Component.Params, "Input")
        for j in range(len(params)):
            Y_cord = params[j].Attributes.InputGrip.Y
            X_cord = params[j].Attributes.Pivot.X
            input_indx = j
            if "i_value_type" == params[j].NickName:
                add_str_valuelist(
                    ghenv.Component,
                    self.poss_value_types,
                    "DF_value_t",
                    input_indx, X_cord, Y_cord)
            if "i_palette" == params[j].NickName:
                add_str_valuelist(
                    ghenv.Component,
                    self.poss_palettes,
                    "DF_palette",
                    input_indx, X_cord, Y_cord)

    def RunScript(self,
        i_value_type: str,
        i_palette: str,
        i_upper_threshold: float,
        i_lower_threshold: float,
        i_legend_height: float,
        i_legend_width: float,
        i_legend_plane: rg.Plane,
        i_histogram_scale_factor: float):

        """
        Compiles all the visualization settings to feed to the visualization component

        :param i_value_type: selected type indicates Which values to display. Possible values: "dist", "RMSE", "MAX", "MIN", "STD"
        :param i_palette: Select a color palette to map the values to. Possible values: "Jet", "Rainbow", "RdPu", "Viridis"
        :param i_upper_threshold: Thresholds the values with a maximum value
        :param i_lower_threshold: Thresholds the values with a minimum value
        :param i_legend_height: the total height of the legend
        :param i_legend_width: the total width of the legend
        :param i_legend_plane: the construction plane of the legend
        :param i_histogram_scale_factor: Scales the height of the histogram with a factor

        :returns o_viz_settings: the results of the comparison all in one object
        """
        # set default values
        if i_value_type is not None:
            if i_value_type not in self.poss_value_types:
                ghenv.Component.AddRuntimeMessage(RML.Warning, "Possible values for i_value_type are: dist, RMSE, MAX, MIN, STD")
                return None
        else:
            i_value_type = "Dist"
        if i_palette is not None:
            if i_palette not in self.poss_palettes:
                ghenv.Component.AddRuntimeMessage(RML.Warning, "Possible values for i_palette are: Jet, Rainbow, RdPu, Viridis")
                return None
        else:
            i_palette = "Jet"
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

# if __name__ == "__main__":
#     com = DFVisualizationSettings()
#     o_viz_settings = com.RunScript(
#         i_value_type,
#         i_palette,
#         i_upper_threshold,
#         i_lower_threshold,
#         i_legend_height,
#         i_legend_width,
#         i_legend_plane,
#         i_histogram_scale_factor
#         )