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

import numpy as np


class DFCADSegmentator(component):
    def RunScript(self,
        i_clouds : typing.List[rg.PointCloud],
        i_assembly : diffCheck.df_geometries.DFAssembly,
        i_angle_threshold : float,
        i_association_threshold : float
    ) -> rg.PointCloud:
        """
        @param i_meshes : the beams (to be converted)
        @param i_angle_threshold : from 0 to 1, it's the sin value. The closer to 0 the less permissive and viceversa to 1.
        @param i_association_threshold: from 0 to infinite. By default 0.5. The closer to 0 the less permissive your point 
        inclusion will be, the higher the value the opposite.

        @return o_clusters : the clusters of the beams
        """
        # the final rhino cloud clusters associated to the beams
        o_clusters = []
        # the df cloud clusters
        df_clusters = []
        # we make a deepcopy of the input clouds because 
        df_clouds = [df_cvt_bindings.cvt_rhcloud_2_dfcloud(cloud.Duplicate()) for cloud in i_clouds]

        df_beams = i_assembly.beams
        df_beams_meshes = []

        for df_b in df_beams:
            rh_b_mesh_faces = [df_b_f.to_mesh() for df_b_f in df_b.side_faces]
            df_b_mesh_faces = [df_cvt_bindings.cvt_rhmesh_2_dfmesh(rh_b_mesh_face) for rh_b_mesh_face in rh_b_mesh_faces]
            df_beams_meshes.append(df_b_mesh_faces)

            df_asssociated_cluster = dfb_segmentation.DFSegmentation.associate_clusters(
                reference_mesh=df_b_mesh_faces,
                unassociated_clusters=df_clouds,
                angle_threshold=i_angle_threshold,
                association_threshold=i_association_threshold
            )

            # TODO: get rid, this is for debugging
            # nbr_total_df_clouds_pts = 0
            # for df_cloud in df_clouds:
            #     nbr_total_df_clouds_pts += df_cloud.get_num_points()
            # print("Total number of points in all clouds: ", nbr_total_df_clouds_pts)

            # FIXME: this is returing empty clusters
            # print(df_asssociated_cluster.has_points())
            if df_asssociated_cluster.has_points():
                df_clusters.append(df_asssociated_cluster)

        # FIXME: the refiner is crashing the script
        # dfb_segmentation.DFSegmentation.clean_unassociated_clusters(
        #         unassociated_clusters=df_clouds,
        #         associated_clusters=df_clusters,
        #         reference_mesh=df_beams_meshes,
        #         angle_threshold=i_angle_threshold,
        #         association_threshold=i_association_threshold
        #     )

        o_clusters = [df_cvt_bindings.cvt_dfcloud_2_rhcloud(cluster) for cluster in df_clusters]

        return o_clusters

if __name__ == "__main__":
    com = DFCADSegmentator()
    o_clusters = com.RunScript(
        i_clouds,
        i_assembly,
        i_angle_threshold,
        i_association_threshold
        )