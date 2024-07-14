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
        o_clusters = []

        df_clouds = [df_cvt_bindings.cvt_rhcloud_2_dfcloud(cloud) for cloud in i_clouds]
        # df_meshes = [df_cvt_bindings.cvt_rhmesh_2_dfmesh(mesh) for mesh in i_meshes]

        df_beams = i_assembly.beams
        rh_beams_meshes = []
        for df_b in df_beams:
            #TODO: check this function to have a better triangluation of the mesh with the parameters
            rh_b_mesh_faces = [df_b_f.to_mesh() for df_b_f in df_b.side_faces]
            # rh_b_mesh_faces = [df_b_f.to_brep_face() for df_b_f in df_b.side_faces]

            # df_b_mesh_faces = [df_cvt_bindings.cvt_rhmesh_2_dfmesh(rh_b_mesh_face) for rh_b_mesh_face in rh_b_mesh_faces]
            
            
            # _ = [rh_beams_meshes.append(m) for m in rh_b_mesh_faces]

            for m in rh_b_mesh_faces:
                # print(type(m))
                rh_beams_meshes.append(m)

            # # convert df_b_mesh_faces to numpy array
            # # get the point clouds corresponding to the beams
            # df_asssociated_clusters : List[dfCloud] = dfb_segmentation.DFSegmentation.associate_clusters(
            #     reference_mesh=df_b_mesh_faces,
            #     unassociated_clusters=df_clouds,
            #     angle_threshold=i_angle_threshold,
            #     association_threshold=i_association_threshold
            # )

            # break

        print("test2")

        return rh_beams_meshes

if __name__ == "__main__":
    com = DFCADSegmentator()
    o_clusters = com.RunScript(
        i_clouds,
        i_assembly,
        i_angle_threshold,
        i_association_threshold
        )