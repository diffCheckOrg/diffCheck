#! python3

from ghpythonlib.componentbase import executingcomponent as component

from diffCheck import df_cvt_bindings
from diffCheck import df_visualization
from diffCheck.df_visualization import DFVizSettings
from diffCheck.df_error_estimation import DFVizResults, DFInvalidData

class DFVisualization(component):
    def RunScript(self,
                  i_result: DFVizResults,
                  i_viz_settings: DFVizSettings):

        if i_result is None or i_viz_settings is None:
            return None, None, None

        # make a DFVizResult copy to avoid modifying the original result to be exported in csv
        result_cp = DFVizResults(i_result.assembly)
        exclude_indices = [idx for idx, sanity_val in enumerate(i_result.sanity_check) if sanity_val.value != DFInvalidData.VALID.value]
        result_cp.source = [val for idx, val in enumerate(i_result.source) if idx not in exclude_indices]
        result_cp.target = [val for idx, val in enumerate(i_result.target) if idx not in exclude_indices]
        result_cp.distances = [val for idx, val in enumerate(i_result.distances) if idx not in exclude_indices]
        result_cp.distances_mean = [val for idx, val in enumerate(i_result.distances_mean) if idx not in exclude_indices]
        result_cp.distances_rmse = [val for idx, val in enumerate(i_result.distances_rmse) if idx not in exclude_indices]
        result_cp.distances_max_deviation = [val for idx, val in enumerate(i_result.distances_rmse) if idx not in exclude_indices]
        result_cp.distances_min_deviation = [val for idx, val in enumerate(i_result.distances_min_deviation) if idx not in exclude_indices]
        result_cp.distances_sd_deviation = [val for idx, val in enumerate(i_result.distances_sd_deviation) if idx not in exclude_indices]

        values, min_value, max_value = result_cp.filter_values_based_on_valuetype(i_viz_settings)

        # check if result_cp.source is a list of pointclouds or a mesh
        if result_cp.is_source_cloud:
            o_source = [df_cvt_bindings.cvt_dfcloud_2_rhcloud(src) for src in result_cp.source]
            o_colored_geo = [df_visualization.color_rh_pcd(src, dist, min_value, max_value, i_viz_settings.palette) for src, dist in zip(o_source, values)]
        else:
            o_source = result_cp.source
            o_colored_geo = [df_visualization.color_rh_mesh(src, dist, min_value, max_value, i_viz_settings.palette) for src, dist in zip(o_source, values)]

        o_legend = df_visualization.create_legend(min_value,
                                                  max_value,
                                                  i_viz_settings.palette,
                                                  steps=10,
                                                  plane=i_viz_settings.legend_plane,
                                                  width=i_viz_settings.legend_width,
                                                  total_height=i_viz_settings.legend_height)

        if len(result_cp.source) > 1 and i_viz_settings.one_histogram_per_item:
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
