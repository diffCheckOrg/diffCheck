#! python3
"""
    This module contains the utility functions to compute the difference between source and target
"""

import numpy as np


def cloud_2_cloud_distance(source, target, signed=False):
    """
        Compute the Euclidean distance for every point of a source pcd to its closest point on a target pointcloud
    """
    distances = np.full(len(source.points), np.inf)

    for i in range(len(source.points)):

        dists = np.linalg.norm(np.asarray(target.points) - np.asarray(source.points)[i], axis=1)
        distances[i] = np.min(dists)

        # determine whether the point on the source cloud is in the same direction as the normal of the corresponding point on the target pcd
        if signed:
            closest_idx = np.argmin(dists)
            # direction from target to source
            direction = source.points[i] - target.points[closest_idx]
            distances[i] *= np.sign(np.dot(direction, target.normals[closest_idx]))

    return distances


def cloud_2_mesh_distance(source, target):

    distances = np.ones(len(source.points), dtype=float)

    return distances


def compute_mse(distances):
    """
        Calculate mean squared distance
    """
    mse = np.sqrt(np.mean(distances ** 2))

    return mse


def compute_max_deviation(distances):
    """
        Calculate max deviation of distances
    """
    max_deviation = np.max(distances)

    return max_deviation


def compute_min_deviation(distances):
    """
        Calculate min deviation of distances
    """

    min_deviation = np.min(distances)

    return min_deviation


def compute_standard_deviation(distances):
    """
        Calculate standard deviation of distances
    """
    standard_deviation = np.std(distances)

    return standard_deviation
