#! python3
"""
    This module contains the utility functions to compute the difference between source and target
"""

import numpy as np
import open3d as o3d
from diffCheck import diffcheck_bindings
import Rhino.Geometry as rg

def cloud_2_cloud_distance(source, target, signed=False):
    """
        Compute the Euclidean distance for every point of a source pcd to its closest point on a target pointcloud
    """
    distances_to_target = np.asarray(source.compute_distance(target))
    distances_to_source = np.asarray(target.compute_distance(source))

    return DFVizResults(source, target, distances_to_target, distances_to_source)


def cloud_2_mesh_distance(source, target, signed=False):
    """
        Calculate the distance between every point of a source pcd to its closest point on a target DFMesh
    """

    # for every point on the PCD compute the point_2_mesh_distance
    if signed:
        distances = np.asarray(target.compute_distance(source, is_abs=False))
    else:
        distances = np.asarray(target.compute_distance(source, is_abs=True))

    return distances

def cloud_2_rhino_mesh_distance(source, target, signed=False):
    """
        Calculate the distance between every point of a source pcd to its closest point on a target Rhino Mesh
    """

    #for every point on the point cloud find distance to mesh
    distances = []

    for p in source.points:

        rhp = rg.Point3d(p[0], p[1], p[2])
        closest_meshPoint = target.ClosestMeshPoint(rhp, 1000)
        closest_point = closest_meshPoint.Point
        face_Index = closest_meshPoint.FaceIndex
        distance = rhp.DistanceTo(closest_point)

        if signed:
            # Calculate the direction from target to source
            direction = rhp - closest_point
            # Calculate the signed distance
            normal = target.NormalAt(closest_meshPoint)
            dot_product = direction * normal
            if dot_product < 0:
                distance = -distance

        distances.append(distance)

    return np.asarray(distances)


# def compute_mse(distances):
#     """
#         Calculate mean squared distance
#     """
#     mse = np.sqrt(np.mean(distances ** 2))

#     return mse


# def compute_max_deviation(distances):
#     """
#         Calculate max deviation of distances
#     """
#     max_deviation = np.max(distances)

#     return max_deviation


# def compute_min_deviation(distances):
#     """
#         Calculate min deviation of distances
#     """

#     min_deviation = np.min(distances)

#     return min_deviation


# def compute_standard_deviation(distances):
#     """
#         Calculate standard deviation of distances
#     """
#     standard_deviation = np.std(distances)

#     return standard_deviation

class DFVizResults:
    """
    This class compiles the resluts of the error estimation into one object
    """

    def __init__(self, source, target, distances_to_target, distances_to_source):

        self.source = source
        self.target = target

        self.distances_to_target_mse = np.sqrt(np.mean(distances_to_target ** 2))
        self.distances_to_target_max_deviation = np.max(distances_to_target)
        self.distances_to_target_min_deviation = np.min(distances_to_target)
        self.distances_to_target_sd_deviation = np.std(distances_to_target)
        self.distances_to_target = distances_to_target.tolist()

        self.distances_to_source_mse = np.sqrt(np.mean(distances_to_source ** 2))
        self.distances_to_source_max_deviation = np.max(distances_to_source)
        self.distances_to_source_min_deviation = np.min(distances_to_source)
        self.distances_to_source_sd_deviation = np.std(distances_to_source)
        self.distances_to_source = distances_to_source.tolist()

