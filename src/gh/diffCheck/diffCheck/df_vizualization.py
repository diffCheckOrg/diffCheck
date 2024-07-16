#! python3
"""
    This module contains the utility functions to vizualize differences
"""

import numpy as np
import open3d as o3d
from diffCheck import diffcheck_bindings
import Rhino.Geometry as rg
import System.Drawing

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


def interpolate_color(color1, color2, t):
    """Interpolate between two colors."""

    r = int(color1.R + (color2.R - color1.R) * t)
    g = int(color1.G + (color2.G - color1.G) * t)
    b = int(color1.B + (color2.B - color1.B) * t)
    return System.Drawing.Color.FromArgb(r, g, b)


def value_to_color(value, min_value, max_value):
    """Map a value to a color based on a spectral colormap."""

    # Define the spectral colormap (simplified)
    colormap = [
        System.Drawing.Color.FromArgb(0, 0, 255),  # Blue
        System.Drawing.Color.FromArgb(0, 255, 255),  # Cyan
        System.Drawing.Color.FromArgb(0, 255, 0),  # Green
        System.Drawing.Color.FromArgb(255, 255, 0),  # Yellow
        System.Drawing.Color.FromArgb(255, 0, 0),  # Red
        System.Drawing.Color.FromArgb(255, 0, 255)  # Magenta
    ]

    # Normalize the value within the range
    if min_value == max_value:
        t = 0.5
    else:
        t = (value - min_value) / (max_value - min_value)

    # Determine the segment in the colormap
    n = len(colormap) - 1
    idx = int(t * n)
    if idx >= n:
        idx = n - 1
    t = (t * n) - idx

    # Interpolate between the two colors
    color1 = colormap[idx]
    color2 = colormap[idx + 1]

    return interpolate_color(color1, color2, t)


def add_color(pcd, values, min_value, max_values):

    for i, p in enumerate(pcd):
        mapped_color = value_to_color(values[i], min_value, max_values)
        p.Color = mapped_color
    return pcd
