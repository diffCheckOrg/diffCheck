#! python3

import typing

import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component


import diffCheck
import diffCheck.df_geometries
from diffCheck.diffcheck_bindings import dfb_segmentation

from diffCheck import df_cvt_bindings



class DFCADSegmentator(component):
    def RunScript(self,
        i_clouds : typing.List[rg.PointCloud],
        i_assembly : diffCheck.df_geometries.DFAssembly,
        i_angle_threshold : float,
        i_association_threshold : float
    ) -> rg.PointCloud:
        o_clusters = []
        df_clusters = []
        # we make a deepcopy of the input clouds
        df_clouds = [df_cvt_bindings.cvt_rhcloud_2_dfcloud(cloud.Duplicate()) for cloud in i_clouds]

        df_beams = i_assembly.beams
        df_beams_meshes = []
        rh_beams_meshes = []

        for df_b in df_beams:
            rh_b_mesh_faces = [df_b_f.to_mesh() for df_b_f in df_b.side_faces]
            df_b_mesh_faces = [df_cvt_bindings.cvt_rhmesh_2_dfmesh(rh_b_mesh_face) for rh_b_mesh_face in rh_b_mesh_faces]
            df_beams_meshes.append(df_b_mesh_faces)
            rh_beams_meshes.append(rh_b_mesh_faces)

            # different association depending on the type of beam
            df_asssociated_cluster = dfb_segmentation.DFSegmentation.associate_clusters(
                is_cylinder=df_b.is_cylinder,
                reference_mesh=df_b_mesh_faces,
                unassociated_clusters=df_clouds,
                angle_threshold=i_angle_threshold,
                association_threshold=i_association_threshold
                )
            df_clusters.append(df_asssociated_cluster)

        # clean the unassociated clusters depending on the type of assembly
        if i_assembly.contains_cylinders:
            dfb_segmentation.DFSegmentation.clean_unassociated_clusters(
                is_cylinder=True,
                unassociated_clusters=df_clouds,
                associated_clusters=df_clusters,
                reference_mesh=df_beams_meshes,
                angle_threshold=i_angle_threshold,
                association_threshold=i_association_threshold
            )
        else:
            dfb_segmentation.DFSegmentation.clean_unassociated_clusters(
                is_cylinder=False,
                unassociated_clusters=df_clouds,
                associated_clusters=df_clusters,
                reference_mesh=df_beams_meshes,
                angle_threshold=i_angle_threshold,
                association_threshold=i_association_threshold
            )

        o_clusters = [df_cvt_bindings.cvt_dfcloud_2_rhcloud(cluster) for cluster in df_clusters]

        return o_clusters
