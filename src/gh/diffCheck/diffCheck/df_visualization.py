#! python3
"""
    This module contains the utility functions to visualize differences
"""
import Rhino
import scriptcontext as sc
import Rhino.Geometry as rg
from System.Drawing import Color
from diffCheck import df_visualization


class DFVizSettings:
    """
    This class compiles the settings for the visualization into one object
    """

    def __init__(self,
        valueType,
        palette,
        upper_threshold,
        lower_threshold,
        legend_height,
        legend_width,
        legend_plane,
        histogram_scale_factor):

        self.valueType = valueType
        self.palette = df_visualization.DFColorMap(palette)
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold
        self.legend_height = legend_height
        self.legend_width = legend_width
        self.legend_plane = legend_plane
        self.histogram_scale_factor = histogram_scale_factor

        self.str_repr = f"DFVizSettings: \n\t- Value type: {self.valueType}\n\t- Palette: {self.palette}\n\t- Upper threshold: {self.upper_threshold}\n\t- Lower threshold: {self.lower_threshold}\n\t- Legend height: {self.legend_height}\n\t- Legend width: {self.legend_width}\n\t- Legend plane: {self.legend_plane}\n\t- Histogram scale factor: {self.histogram_scale_factor}"

    def __repr__(self):
        return self.str_repr
    def __str__(self):
        return self.str_repr

class DFColorMap:
    """
    This class defines different colormaps for visualization purposes
    It allows selection of a colormap by name and initializes the corresponding color values.
    """

    def __init__(self, name):
        self.name = name
        if self.name == "Jet":
            self.colors = [
                Color.FromArgb(0, 0, 255),  # Blue
                Color.FromArgb(0, 255, 255),  # Cyan
                Color.FromArgb(0, 255, 0),  # Green
                Color.FromArgb(255, 255, 0),  # Yellow
                Color.FromArgb(255, 0, 0),  # Red
            ]
        elif self.name == "Rainbow":
            self.colors = [
                Color.FromArgb(127, 0, 255),
                Color.FromArgb(0, 180, 235),
                Color.FromArgb(128, 254, 179),
                Color.FromArgb(255, 178, 96),
                Color.FromArgb(255, 6, 3)
            ]
        elif self.name == "RdPu":
            self.colors = [
                Color.FromArgb(254, 246, 242),
                Color.FromArgb(251, 196, 191),
                Color.FromArgb(246, 103, 160),
                Color.FromArgb(172, 1, 125),
                Color.FromArgb(76, 0, 106)
            ]
        elif self.name == "Viridis":
            self.colors = [
                Color.FromArgb(68, 3, 87),
                Color.FromArgb(58, 82, 139),
                Color.FromArgb(32, 144, 140),
                Color.FromArgb(94, 201, 97),
                Color.FromArgb(248, 230, 33)
            ]

    def interpolate_color(self, color1, color2, t):
        """
        Interpolate between two colors.
        """

        r = int(color1.R + (color2.R - color1.R) * t)
        g = int(color1.G + (color2.G - color1.G) * t)
        b = int(color1.B + (color2.B - color1.B) * t)

        return Color.FromArgb(r, g, b)

    def value_to_color(self, value, min_value, max_value):
        """
        Map a value to a color based on a colormap.
        """

        if value < min_value:
            value = min_value
        elif value > max_value:
            value = max_value

        colormap = self.colors

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

        return self.interpolate_color(color1, color2, t)


def color_rh_pcd(pcd, values, min_value, max_value, palette):
    """
    Colors a point cloud data based on given values and palette.
    """

    for i, p in enumerate(pcd):
        # check if values is a list
        if isinstance(values, list):
            mapped_color = palette.value_to_color(values[i], min_value, max_value)
        else:
            mapped_color = palette.value_to_color(values, min_value, max_value)

        p.Color = mapped_color

    return pcd


def color_rh_mesh(mesh, values, min_value, max_value, palette):
    """
    Colors a mesh based on given values and palette.
    """

    mesh.VertexColors.Clear()

    for i, vertex in enumerate(mesh.Vertices):
        # check if values is a list
        if isinstance(values, list):
            mapped_color = palette.value_to_color(values[i], min_value, max_value)
        else:
            mapped_color = palette.value_to_color(values, min_value, max_value)
        mesh.VertexColors.Add(mapped_color.R, mapped_color.G, mapped_color.B)

    return mesh


def create_legend(min_value, max_value, palette, steps=10, plane=rg.Plane.WorldXY,
                  width=0.5, total_height=10, spacing=0):
    """
    Create a legend in Rhino with colored hatches and text labels.
    """

    height = total_height/steps

    legend_geometry = []
    rect_pts = []
    previous_color = None

    RhinoDoc = sc.doc
    if RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Meters:
        unit_str = "[m]"
    elif RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Centimeters:
        unit_str = "[cm]"
    elif RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Millimeters:
        unit_str = "[mm]"
    elif RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Inches:
        unit_str = "[in]"
    elif RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Feet:
        unit_str = "[ft]"
    else:
        unit_str = "[yd]"

    # Add the unit label at the top of the legend
    units_pt = rg.Point3d(0.5 * width , (steps + 1) * (height + spacing) - 0.5*height, 0)
    units_text_entity = rg.TextEntity()
    units_text_entity.Plane = rg.Plane(units_pt, rg.Vector3d.ZAxis)
    units_text_entity.Text = unit_str
    units_text_entity.TextHeight = height / 5
    units_text_entity.Justification = rg.TextJustification.MiddleCenter
    units_text_entity.DimensionLengthDisplay = Rhino.DocObjects.DimensionStyle.LengthDisplay.Millmeters
    legend_geometry.append(units_text_entity)

    for i in range(steps+1):

        value = min_value + (max_value - min_value) * i / steps
        color = palette.value_to_color(value, min_value, max_value)

        if i > 0:
            mesh = rg.Mesh()
            for pt in rect_pts:
                mesh.Vertices.Add(pt)

            mesh.Faces.AddFace(0, 1, 2, 3)
            # color mesh
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
        # decide on resolution based on document units
        if RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Meters:
            text_entity.Text = f"{value:.4f}"
        elif RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Centimeters:
            text_entity.Text = f"{value:.3f}"
        elif RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Millimeters:
            text_entity.Text = f"{value:.2f}"
        elif RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Inches:
            text_entity.Text = f"{value:.2f}"
        elif RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Feet:
            text_entity.Text = f"{value:.2f}"
        elif RhinoDoc.ModelUnitSystem == Rhino.UnitSystem.Yards:
            text_entity.Text = f"{value:.2f}"

        text_entity.TextHeight = height / 5
        #match grasshopper display to default
        text_entity.DimensionLengthDisplay = Rhino.DocObjects.DimensionStyle.LengthDisplay.Millmeters
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


def create_histogram(values, min_value, max_value, res=100, steps=10,
                     plane=rg.Plane.WorldXY, total_height=10,
                     scaling_factor=0.01, spacing=0):
    """
    Create a histogram in Rhino with a polyline representing value frequencies.
    """

    height = total_height/res

    histogram_geometry = []

    # Calculate the size of each bin
    bin_size = (max_value - min_value) / res

    # Initialize the frequency counts for each bin
    frequencies = [0] * (res + 1)

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
    max_frequency = max(frequencies)

    for i in range(res+1):

        bar_height = frequencies[i] * scaling_factor
        points.append(rg.Point3d(- bar_height, i * (spacing + height), 0))

    # Create the polyline and add it to the histogram geometry
    polyline = rg.Curve.CreateInterpolatedCurve(points, 1)
    histogram_geometry.append(polyline)

    # Create rectangles to extend the value axis for better visualization
    for i in range(steps):
        rect_pts = [
            rg.Point3d(0, i * (total_height/steps + spacing), 0),
            rg.Point3d(-max_frequency*scaling_factor, i * (total_height/steps + spacing), 0),
            rg.Point3d(-max_frequency*scaling_factor, (i + 1) * total_height/steps + i * spacing, 0),
            rg.Point3d(0, (i + 1) * total_height/steps + i * spacing, 0),
        ]
        polyline = rg.Polyline(rect_pts)
        histogram_geometry.append(polyline.ToPolylineCurve())

    # Create the x-axis label only for the highest value (100%)
    highest_value_pt = rg.Point3d(-max_frequency*scaling_factor - (total_height/steps)/5, -total_height/steps, 0)
    highest_value_text = rg.TextEntity()
    highest_value_text.Plane = rg.Plane(highest_value_pt, rg.Vector3d.YAxis, -rg.Vector3d.XAxis)  # Align text along Y-axis
    highest_value_text.Text = str(max_frequency) + "%"
    highest_value_text.TextHeight = (total_height/steps) / 5
    highest_value_text.DimensionLengthDisplay = Rhino.DocObjects.DimensionStyle.LengthDisplay.Millmeters
    histogram_geometry.append(highest_value_text)

    if plane != rg.Plane.WorldXY:
        trans = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, plane)
        for geo in histogram_geometry:
            geo.Transform(trans)

    return histogram_geometry
