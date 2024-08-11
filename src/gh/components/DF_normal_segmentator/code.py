#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
import diffCheck.df_geometries
from diffCheck.diffcheck_bindings import dfb_segmentation

from diffCheck import df_cvt_bindings


class DFCloudNormalSegmentator(component):
    def RunScript(self,
        i_cloud,
        i_normal_threshold_degree=None,
        i_min_cluster_size=None,
        i_use_knn_neighborhood=None,
        i_knn_neighborhood_size=None,
        i_radius_neighborhood_size=None
    ) -> rg.PointCloud:
        o_clusters = []
        df_cloud = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud)

        if i_normal_threshold_degree is None:
            i_normal_threshold_degree = 20
        if i_min_cluster_size is None:
            i_min_cluster_size = 10
        if i_use_knn_neighborhood is None:
            i_use_knn_neighborhood = True
        if i_knn_neighborhood_size is None:
            i_knn_neighborhood_size = 30
        if i_radius_neighborhood_size is None:
            i_radius_neighborhood_size = 0.1

        o_clusters = dfb_segmentation.DFSegmentation.segment_by_normal(
            point_cloud=df_cloud,

            normal_threshold_degree=i_normal_threshold_degree,
            min_cluster_size=i_min_cluster_size,
            use_knn_neighborhood=i_use_knn_neighborhood,
            knn_neighborhood_size=i_knn_neighborhood_size,
            radius_neighborhood_size=i_radius_neighborhood_size
        )

        return [df_cvt_bindings.cvt_dfcloud_2_rhcloud(cluster) for cluster in o_clusters]