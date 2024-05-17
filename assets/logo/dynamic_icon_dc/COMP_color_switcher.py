#! python3

import os

import Rhino
import Rhino.Geometry as rg

import colorsys
import System


def get_diff_color(est_area, gt_area):
    # Calculate the ratio of estimated area to ground truth area
    ratio = est_area / gt_area if gt_area != 0 else 1

    # Clamp the ratio between 0 and 1
    ratio = max(0, min(ratio, 1))

    # Generate a color that transitions from green to red based on the ratio
    # In the HSV color model, green is at hue = 2/3 and red is at hue = 0
    hue = 2 / 3 * ratio

    # Convert the HSV color to RGB
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    g, r, b = b, g, r  # Corrected order

    # Convert the RGB color to a System.Drawing.Color
    color = System.Drawing.Color.FromArgb(int(255 * r), int(255 * g), int(255 * b))  # Corrected order

    return color

clr = get_diff_color(i_est_area, i_gt_area)
o_clr = clr