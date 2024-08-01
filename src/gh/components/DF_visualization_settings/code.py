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


        
# FIXME: rearrange position
poss_value_types = ["Dist", "RMSE", "MAX", "MIN", "STD"]
poss_value_types_dict = {
    0: "Dist",
    1: "RMSE",
    2: "MAX",
    3: "MIN",
    4: "STD"
}
poss_palettes = ["Jet", "Rainbow", "RdPu", "Viridis"]
def add_valuelist(self, nickname, indx, Y):
    param = ghenv.Component.Params.Input[indx]
    if param.SourceCount == 0:
        valuelist = Grasshopper.Kernel.Special.GH_ValueList()
        valuelist.NickName = nickname
        selected = valuelist.FirstSelectedItem
        valuelist.ListItems.Clear()
        Keys = ["Dist", "RMSE", "MAX", "MIN", "STD"]
        Values = ["Dist", "RMSE", "MAX", "MIN", "STD"]
        # for key, item in poss_value_types_dict.items():
        for k,v in zip(Keys,Values):
            vli = gh.Kernel.Special.GH_ValueListItem(str(k),str('"' + v + '"'))
            # vli = gh.Kernel.Special.GH_ValueListItem("".join(item),"".join(key))
            valuelist.ListItems.Add(vli)
        if selected in Keys:
            valuelist.SelectItem(Keys.index(selected))
        valuelist.ExpireSolution(True)

        
        valuelist.CreateAttributes()
        valuelist.Attributes.Pivot = System.Drawing.PointF(
            self.Attributes.InputGrip.X - valuelist.Attributes.Bounds.Width - 10,
            Y - valuelist.Attributes.Bounds.Height / 2
            )
        # FIXME: the problem is that the valuelist does not have values, it has ti be recomputed
        valuelist.Attributes.ExpireLayout();
        Grasshopper.Instances.ActiveCanvas.Document.AddObject(valuelist, False)
        self.Params.Input[indx].AddSource(valuelist)

class VisualizationSettings(component):
    def BeforeRunScript(self):
        params = getattr(ghenv.Component.Params, "Input")
        for j in range(len(params)):
            if "i_value_type" == params[j].NickName:
                # if params[j].Attributes.InputGrip.Y == 10:
                #     ghenv.Component.ExpireSolution(True)
                Y_cord = params[j].Attributes.InputGrip.Y
                input_indx = j
                add_valuelist(ghenv.Component, "nicknametest", input_indx, Y_cord)



    def RunScript(self,
        i_value_type: int,
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

        print(f"DEBUG>>>i_value_type: {i_value_type}")

        # set default values
        # FIXME: the none check has to be kept
        if i_value_type is not None:
            if i_value_type not in poss_value_types:
                ghenv.Component.AddRuntimeMessage(RML.Warning, "Possible values for i_value_type are: dist, RMSE, MAX, MIN, STD")
                return None
        else:
            i_value_type = "Dist"
        if i_palette is not None:
            if i_palette not in poss_palettes:
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

        # print(i_value_type)
        return i_value_type
        # return o_viz_settings

# if __name__ == "__main__":
#     com = VisualizationSettings()
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