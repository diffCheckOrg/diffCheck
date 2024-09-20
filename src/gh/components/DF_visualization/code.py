#! python3

import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component


from diffCheck import df_cvt_bindings
from diffCheck import df_visualization
from diffCheck.df_visualization import DFVizSettings
from diffCheck.df_error_estimation import DFVizResults
from diffCheck import diffcheck_bindings

class DFVisualization(component):
    def RunScript(self,
                  i_result: DFVizResults,
                  i_viz_settings: DFVizSettings):
 
        values, min_value, max_value = i_result.filter_values_based_on_valuetype(i_viz_settings)

        # check if i_result.source is a list of pointclouds or a mesh
        if type(i_result.source[0]) is diffcheck_bindings.dfb_geometry.DFPointCloud:

            # convert to Rhino PCD
            o_source = [df_cvt_bindings.cvt_dfcloud_2_rhcloud(src) for src in i_result.source]

            # color geometry
            o_colored_geo = [df_visualization.color_rh_pcd(src, dist, min_value, max_value, i_viz_settings.palette) for src, dist in zip(o_source, values)]

        elif type(i_result.source[0]) is rg.Mesh:
            # convert to Rhino Mesh
            o_source = i_result.source

            # color geometry
            o_colored_geo = [df_visualization.color_rh_mesh(src, dist, min_value, max_value, i_viz_settings.palette) for src, dist in zip(o_source, values)]

        o_legend = df_visualization.create_legend(min_value,
                                                  max_value,
                                                  i_viz_settings.palette,
                                                  steps=10,
                                                  plane=i_viz_settings.legend_plane,
                                                  width=i_viz_settings.legend_width,
                                                  total_height=i_viz_settings.legend_height)

        # add option to create a histogram for each item

        if len(i_result.source) > 1 and i_viz_settings.one_histogram_per_item:
            multiple_curves = True
        else:
            multiple_curves = False

        o_histogram = df_visualization.create_histogram(values,
                                                        min_value,
                                                        max_value,
                                                        res=100,
                                                        steps=10,
                                                        plane=i_viz_settings.legend_plane,
                                                        total_height=i_viz_settings.legend_height,
                                                        scaling_factor=i_viz_settings.histogram_scale_factor,
                                                        multiple_curves = multiple_curves)

        return o_colored_geo, o_legend, o_histogram

# if __name__ == "__main__":
#     com = DFVisualization()
#     o_colored_geo, o_legend, o_histogram = com.RunScript(
#         i_result,
#         i_viz_settings
#         )
