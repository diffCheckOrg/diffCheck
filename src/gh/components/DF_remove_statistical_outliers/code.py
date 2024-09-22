#! python3

import Rhino
from ghpythonlib.componentbase import executingcomponent as component

import diffCheck.df_cvt_bindings as cvt

class DFRemoveStatisticalOutliers(component):
    def RunScript(self, i_cloud: Rhino.Geometry.PointCloud, i_knn : int, i_ratio : float):
        if i_cloud is None or i_ratio is None or i_knn is None:
            return None

        df_cloud = cvt.cvt_rhcloud_2_dfcloud(i_cloud)
        df_cloud.remove_statistical_outliers(nb_neighbors=i_knn, std_ratio=i_ratio)
        o_cloud = cvt.cvt_dfcloud_2_rhcloud(df_cloud)

        return o_cloud
