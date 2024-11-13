#! python3

from ghpythonlib.componentbase import executingcomponent as component

from diffCheck.df_error_estimation import DFVizResults


class DFImportResults(component):
    def RunScript(self, i_import_path: str):
        if i_import_path is None:
            return None

        o_results = DFVizResults.load_pickle(i_import_path)

        return o_results
