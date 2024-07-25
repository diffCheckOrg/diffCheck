#! python3
"""
    This module contains the utility functions to vizualize differences
"""

import Rhino.Geometry as rg
from System.Drawing import Color
from diffCheck import df_vizualization

class DFVizSettings:
    """
    This class compiles the settings for the vizualization into one object
    """

    def __init__(self, valueType, upper_threshold, lower_threshold, palette, legend_height, legend_width, legend_plane, histogram_scale_factor):

        self.valueType = valueType

        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold
        self.palette = df_vizualization.DFColorMap(palette)
        self.legend_height = legend_height
        self.legend_width = legend_width
        self.legend_plane = legend_plane
        self.histogram_scale_factor = histogram_scale_factor


class DFColorMap:
    """
    This class defines different colormaps for visualization purposes
    It allows selection of a colormap by name and initializes the corresponding color values.
    """

    def __init__(self, name):
        self.names = name
        if name == "Jet":
            self.colors = [
                Color.FromArgb(0, 0, 255),  # Blue
                Color.FromArgb(0, 255, 255),  # Cyan
                Color.FromArgb(0, 255, 0),  # Green
                Color.FromArgb(255, 255, 0),  # Yellow
                Color.FromArgb(255, 0, 0),  # Red
            ]
        elif name == "Rainbow":
            self.colors = [
                Color.FromArgb(127, 0, 255),
                Color.FromArgb(0, 180, 235),
                Color.FromArgb(128, 254, 179),
                Color.FromArgb(255, 178, 96),
                Color.FromArgb(255, 6, 3)
            ]
        elif name == "RdPu":
            self.colors = [
                Color.FromArgb(254, 246, 242),
                Color.FromArgb(251, 196, 191),
                Color.FromArgb(246, 103, 160),
                Color.FromArgb(172, 1, 125),
                Color.FromArgb(76, 0, 106)
            ]
        elif name == "Viridis":
            self.colors = [
                Color.FromArgb(68, 3, 87),
                Color.FromArgb(58, 82, 139),
                Color.FromArgb(32, 144, 140),
                Color.FromArgb(94, 201, 97),
                Color.FromArgb(248, 230, 33)
            ]

def interpolate_color(color1, color2, t):
    """
    Interpolate between two colors.
    """

    r = int(color1.R + (color2.R - color1.R) * t)
    g = int(color1.G + (color2.G - color1.G) * t)
    b = int(color1.B + (color2.B - color1.B) * t)
    return Color.FromArgb(r, g, b)


def value_to_color(value, min_value, max_value, palette):
    """
    Map a value to a color based on a colormap.
    """

    if value < min_value:
        value = min_value
    elif value > max_value:
        value = max_value

    colormap = palette.colors

    # Normalize the value within the range
    if min_value == max_value:
        t = 0.5
    else:
        t = (value - min_value) / (max_value - min_value)

    # Determine the segment in the colormap
    n = len(colormap)- 1
    idx = int(t * n)
    if idx >= n:
        idx = n - 1
    t = (t * n) - idx

    # Interpolate between the two colors
    color1 = colormap[idx]
    color2 = colormap[idx + 1]

    return interpolate_color(color1, color2, t)


def color_pcd(pcd, values, min_value, max_value, palette):
    """
    Colors a point cloud data based on given values and palette.
    """

    for i, p in enumerate(pcd):
        # check if values is a list
        if isinstance(values, list):
            mapped_color = value_to_color(values[i], min_value, max_value, palette)
        else:
            mapped_color = value_to_color(values, min_value, max_value, palette)

        p.Color = mapped_color

    return pcd


def color_mesh(mesh, values, min_value, max_value, palette):
    """
    Colors a mesh based on given values and palette.
    """

    mesh.VertexColors.Clear()
    
    for i, vertex in enumerate(mesh.Vertices):
        # check if values is a list
        if isinstance(values, list):
            mapped_color = value_to_color(values[i], min_value, max_value, palette)
        else:
            mapped_color = value_to_color(values, min_value, max_value, palette)
        mesh.VertexColors.Add(mapped_color.R, mapped_color.G, mapped_color.B)

    return mesh


def create_legend(min_value, max_value, palette, steps=10, plane=rg.Plane.WorldXY,
                  width=0.5, total_height=10, spacing=0):
    """
    Create a legend in Rhino with colored hatches and text labels.
    """

    height = total_height/steps

    legend_geometry = []

    for i in range(steps+1):

        value = min_value + (max_value - min_value) * i / steps
        color = value_to_color(value, min_value, max_value, palette)

        if i > 0:
            mesh = rg.Mesh()
            for pt in rect_pts:
                mesh.Vertices.Add(pt)
            # color mesh
            mesh.Faces.AddFace(0, 1, 2, 3)
            
            mesh.VertexColors.Add(previous_color.R, previous_color.G, previous_color.B)
            mesh.VertexColors.Add(previous_color.R, previous_color.G, previous_color.B)
            mesh.VertexColors.Add(color.R, color.G, color.B)
            mesh.VertexColors.Add(color.R, color.G, color.B)

            polyline = rg.Polyline(rect_pts)

            legend_geometry.append(mesh)
            legend_geometry.append(polyline.ToPolylineCurve())

        text_pt = rg.Point3d(1.25 * width + spacing, i * (height + spacing) + height / 10, 0)
        text_entity = rg.TextEntity()
        text_entity.Plane = rg.Plane(text_pt, rg.Vector3d.ZAxis)
        text_entity.Text = f"{value:.2f}"
        text_entity.TextHeight = height / 5
        legend_geometry.append(text_entity)

        rect_pts = [
            rg.Point3d(0, i * (height + spacing), 0),
            rg.Point3d(0 + width, i * (height + spacing), 0),
            rg.Point3d(0 + width, (i + 1) * height + i * spacing, 0),
            rg.Point3d(0, (i + 1) * height + i * spacing, 0),
        ]

        previous_color = color

    if plane != rg.Plane.WorldXY:
        trans = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, plane)
        for geo in legend_geometry:
            geo.Transform(trans)

    return legend_geometry


def create_histogram(values, min_value, max_value, steps=100, plane=rg.Plane.WorldXY, total_height=10, scaling_factor = 0.01, spacing=0):
    """
    Create a histogram in Rhino with a polyline representing value frequencies.
    """

    height = total_height/steps

    histogram_geometry = []

    # Calculate the size of each bin
    bin_size = (max_value - min_value) / steps

    # Initialize the frequency counts for each bin
    frequencies = [0] * (steps + 1)

    # if values is nested list, flatten it
    if isinstance(values[0], list):
        values = [item for sublist in values for item in sublist]

    # Count the frequencies of values in each bin
    for value in values:
        if value < min_value:
            value = min_value
        elif value > max_value:
            value = max_value
        bin_index = (value - min_value) // bin_size
        bin_index = int(bin_index)
        frequencies[bin_index] += 1

    # Create points for the polyline representing the histogram
    points = []
    for i in range(steps+1):

        bar_height = frequencies[i] * scaling_factor
        points.append(rg.Point3d(- bar_height - (1.5 * height), i * (spacing + height), 0))

    # Create the polyline and add it to the histogram geometry
    polyline = rg.Curve.CreateInterpolatedCurve(points, 1)
    histogram_geometry.append(polyline)

    if plane != rg.Plane.WorldXY:
        trans = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, plane)
        for geo in histogram_geometry:
            geo.Transform(trans)

    return histogram_geometry


def filter_values_based_on_valuetype(results, settings):

    if settings.valueType == "Dist":

        min_value = min(min(sublist) for sublist in results.distances)
        max_value = max(max(sublist) for sublist in results.distances)
        values = results.distances

    elif settings.valueType == "MSE":

        values = results.distances_mse
        min_value = min(values)
        max_value = max(values)
        
    elif settings.valueType == "MAX":

        values = results.distances_max_deviation
        min_value = min(values)
        max_value = max(values)

    elif settings.valueType == "MIN":
        values = results.distances_min_deviation
        min_value = min(values)
        max_value = max(values)

    elif settings.valueType == "STD":

        values = results.distances_sd_deviation
        min_value = min(values)
        max_value = max(values)

    # threshold values
    if settings.lower_threshold is not None:
        min_value = settings.lower_threshold
    if settings.upper_threshold is not None:
        max_value = settings.upper_threshold

    return values, min_value, max_value
