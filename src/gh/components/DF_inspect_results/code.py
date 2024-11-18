#! python3

from ghpythonlib.componentbase import executingcomponent as component


class DFInspectResults(component):
    def RunScript(self, i_results):
        if i_results is None:
            return None

        return i_results.assembly, \
            i_results.source, \
            i_results.target, \
            i_results.distances_mean, \
            i_results.distances_rmse, \
            i_results.distances_max_deviation, \
            i_results.distances_min_deviation, \
            i_results.distances_sd_deviation, \
            i_results.distances
