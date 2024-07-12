#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings
from diffCheck import df_error_estimation


class CloudToMeshDistance(component):
    def RunScript(self,
        i_cloud_source: rg.PointCloud,
        i_beam,
        i_signed_flag: bool):
        """
            The cloud-to-cloud component computes the distance between each point in the source point cloud and its nearest neighbour in thr target point cloud.

            :param i_cloud_source: source point cloud
            :param i_mesh_target: target point cloud to align to

            :return o_distances : list of calculated distances for each point
            :return o_mse: the average squared difference between corresponding points of source and target
            :return o_max_deviation: the max deviation between source and target (Hausdorff Distance)
            :return o_min_deviation: the min deviation between source and target
        """
        if i_cloud_source is None or i_beam is None:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Please provide an object of type point cloud and an object of type mesh to compare")
            return None

        # conversion
        df_cloud_source = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud_source)
        rhino_mesh_target = i_beam.to_mesh()
        df_mesh_target = df_cvt_bindings.cvt_rhmesh_2_dfmesh(rhino_mesh_target)

        # calculate distances
        o_results = df_error_estimation.cloud_2_mesh_distance(df_cloud_source, df_mesh_target, i_signed_flag)

        o_mesh = rhino_mesh_target

        return o_distances.tolist(), o_mse, o_max_deviation, o_min_deviation, o_mesh



if __name__ == "__main__":
    com = CloudToMeshDistance()
    o_distances, o_mse, o_max_deviation, o_min_deviation, o_mesh = com.RunScript(
        i_cloud_source,
        i_mesh_target,
        i_signed_flag
        )