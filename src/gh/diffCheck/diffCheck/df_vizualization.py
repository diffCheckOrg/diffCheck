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


def color_pcd(pcd, values, min_value, max_values):

    for i, p in enumerate(pcd):
        mapped_color = value_to_color(values[i], min_value, max_values)
        p.Color = mapped_color
    return pcd


def create_legend(min_value, max_value, steps=10, base_point=rg.Point3d(0, 0, 0), width=0.5, height=1, spacing=0):
    """
    Create a legend in Rhino with colored hatches and text labels.
    
    Parameters:
    min_value (float): Minimum value for the legend.
    max_value (float): Maximum value for the legend.
    steps (int): Number of steps in the legend.
    base_point (rg.Point3d): The base point where the legend starts.
    width (float): Width of each rectangle.
    height (float): Height of each rectangle.
    spacing (float): Spacing between rectangles.
    """
    x, y, z = base_point.X, base_point.Y, base_point.Z
    
    legend_geometry = []

    for i in range(steps + 1):
        value = min_value + (max_value - min_value) * i / steps
        color = value_to_color(value, min_value, max_value)
        
        rect_pts = [
            rg.Point3d(x, y + i * (height + spacing), z),
            rg.Point3d(x + width, y + i * (height + spacing), z),
            rg.Point3d(x + width, y + (i + 1) * height + i * spacing, z),
            rg.Point3d(x, y + (i + 1) * height + i * spacing, z),
            rg.Point3d(x, y + i * (height + spacing), z)
        ]
        
        mesh = rg.Mesh()
        for pt in rect_pts:
            mesh.Vertices.Add(pt)
        mesh.Faces.AddFace(0, 1, 2, 3)
        mesh.VertexColors.CreateMonotoneMesh(color)

        polyline = rg.Polyline(rect_pts)
        
        legend_geometry.append(mesh)
        
        legend_geometry.append(polyline.ToPolylineCurve())
        
        text_pt = rg.Point3d(x + width + spacing, y + i * (height + spacing) + height / 2, z)
        text_entity = rg.TextEntity()
        text_entity.Plane = rg.Plane(text_pt, rg.Vector3d.ZAxis)
        text_entity.Text = f"{value:.2f}"
        text_entity.TextHeight = height / 2
        legend_geometry.append(text_entity)
    
    return legend_geometry