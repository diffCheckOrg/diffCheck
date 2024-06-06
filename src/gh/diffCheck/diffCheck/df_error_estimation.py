#! python3
"""
    This module contains the utility functions to convert the data between the
    Rhino, the basic diffCheck data structures and the diffCheck bindings.
"""

import Rhino
import Rhino.Geometry as rg
import numpy as np
from diffCheck import diffcheck_bindings

def cloud_2_cloud_distance(source, target):

    # Convert pts to np array and calculate distances
    distances = np.linalg.norm(np.asarray(source.points) - np.asarray(target.points), axis=1)

    return distances

def compute_mse(source, target):
    """
        Calculate mean squared distance
    """
     
    distances = cloud_2_cloud_distance(source, target)
    mse = np.sqrt(np.mean(distances ** 2))

    return mse

def compute_max_deviation(source, target):
    """
        Calculate max deviation of distances
    """
     
    max_deviation = np.max(cloud_2_cloud_distance(source, target))

    return max_deviation



def compute_min_deviation(source, target):
    """
        Calculate min deviation of distances
    """

    max_deviation = np.min(cloud_2_cloud_distance(source, target))

    return min_deviation


def compute_standard_deviation(source, target):
    """
        Calculate standard deviation of distances
    """
     
    std_deviation = np.std(cloud_2_cloud_distance(source, target))

    return standard_deviation