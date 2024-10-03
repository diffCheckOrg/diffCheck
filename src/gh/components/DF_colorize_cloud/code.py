#! python3

import System

import Rhino
from ghpythonlib.componentbase import executingcomponent as component

import numpy as np


class DFColorizeCloud(component):
    def RunScript(self, i_clouds: System.Collections.Generic.List[Rhino.Geometry.PointCloud]):

        if i_clouds is None:
            return None

        for cloud in i_clouds:
            random_color = System.Drawing.Color.FromArgb(
                np.random.randint(0, 255),
                np.random.randint(0, 255),
                np.random.randint(0, 255))
            for j in range(cloud.Count):
                cloud[j].Color = random_color
        return i_clouds
