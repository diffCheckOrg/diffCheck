#! python3
"""
    This module contains the utility functions to convert the data between the
    Rhino, the basic diffCheck data structures and the diffCheck bindings.
"""

import numpy as np
from diffCheck import diffcheck_bindings

def cloud_2_cloud_distance(source, target):

    # Convert pts to np array and calculate distances
    distances = np.linalg.norm(np.asarray(source.points) - np.asarray(target.points), axis=1)

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
