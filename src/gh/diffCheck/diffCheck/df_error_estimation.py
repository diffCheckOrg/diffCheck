#! python3
"""
    This module contains the utility functions to compute the difference between source and target
"""

import numpy as np
import open3d as o3d
from diffCheck import diffcheck_bindings

def cloud_2_cloud_distance(source, target, signed=False):
    """
        Compute the Euclidean distance for every point of a source pcd to its closest point on a target pointcloud
    """
    distances = np.asarray(source.compute_distance(target))

    return distances


def cloud_2_mesh_distance(source, target, signed=False):
    """
        Calculate the distance between every point of a source pcd to its closest point on a target beam
    """

    # for every point on the PCD compute the point_2_mesh_distance
    if signed:
        distances = np.asarray(target.compute_distance(source, is_abs=False))
    else:
        distances = np.asarray(target.compute_distance(source, is_abs=True))

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
