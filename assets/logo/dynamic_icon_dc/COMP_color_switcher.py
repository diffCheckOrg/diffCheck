#! python3

import os

import Rhino
import Rhino.Geometry as rg

import colorsys
import System


import matplotlib.pyplot as plt

def get_diff_color(est_area, gt_area):
    # Calculate the ratio of estimated area to ground truth area
    ratio = est_area / gt_area if gt_area != 0 else 1

    # Clamp the ratio between 0 and 1
    ratio = max(0, min(ratio, 1))

    # Get the magma colormap
    cmap = plt.get_cmap('magma')  # bone, twilight_shifted

    # Get the RGB color from the colormap
    r, g, b, _ = cmap(ratio)

    # Convert the RGB color to a System.Drawing.Color
    color = System.Drawing.Color.FromArgb(int(255 * r), int(255 * g), int(255 * b))

    return color


clr = get_diff_color(i_est_area, i_gt_area)
o_clr = clr