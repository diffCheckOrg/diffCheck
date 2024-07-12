#! python3
"""
    This module contains the utility functions to vizualize differences
"""

import numpy as np
import open3d as o3d
from diffCheck import diffcheck_bindings
import Rhino.Geometry as rg

class DFVizSettings:
    """
    This class compiles the settings for the vizualization into one object
    """

    def __init__(self, source_valueType, target_valueType, upper_threshold, lower_threshold, palette):

        self.source_valueType = source_valueType
        self.target_valueType = target_valueType

        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold
        self.palette = palette
