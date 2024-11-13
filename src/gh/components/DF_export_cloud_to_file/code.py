#! python3

import System

import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
import Grasshopper as gh

from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings


def add_button(self,
    nickname: str,
    indx: int,
    X_param_coord: float,
    Y_param_coord: float,
    X_offset: int=45
    ) -> None:
    """
        Adds a button to the component input

        :param nickname: the nickname of the button
        :param indx: the index of the input parameter
        :param X_param_coord: the x coordinate of the input parameter
        :param Y_param_coord: the y coordinate of the input parameter
        :param X_offset: the offset of the button from the input parameter
    """
    param = ghenv.Component.Params.Input[indx]  # noqa: F821
    if param.SourceCount == 0:
        button = gh.Kernel.Special.GH_ButtonObject()
        button.NickName = ""
        button.Description = ""
        button.CreateAttributes()
        button.Attributes.Pivot = System.Drawing.PointF(
            X_param_coord - (button.Attributes.Bounds.Width) - X_offset,
            Y_param_coord - (button.Attributes.Bounds.Height / 2 - 0.1)
            )
        button.Attributes.ExpireLayout()
        gh.Instances.ActiveCanvas.Document.AddObject(button, False)
        ghenv.Component.Params.Input[indx].AddSource(button)    # noqa: F821

class DFExportCloudToFile(component):
    def __init__(self):
        super(DFExportCloudToFile, self).__init__()
        ghenv.Component.ExpireSolution(True)  # noqa: F821
        ghenv.Component.Attributes.PerformLayout()    # noqa: F821
        params = getattr(ghenv.Component.Params, "Input")    # noqa: F821
        for j in range(len(params)):
            X_cord = params[j].Attributes.Pivot.X
            Y_cord = params[j].Attributes.InputGrip.Y
            if params[j].Name == "i_dump":
                add_button(self, "", j, X_cord, Y_cord)

    def RunScript(self,
        i_dump: bool,
        i_file_path: str,
        i_cloud: rg.PointCloud) -> None:
        if i_dump is None or i_file_path is None or i_cloud is None:
            return None

        # check that the i_file_path is a valid path and it has the .ply extension
        if not i_file_path.endswith(".ply"):
            ghenv.Component.AddRuntimeMessage(RML.Warning, exception)  # noqa: F821
            return None

        if i_dump:
            df_cloud: diffcheck_bindings.dfb_geometry.DFPointCloud = df_cvt_bindings.cvt_rhcloud_2_dfcloud(i_cloud)
            df_cloud.save_to_PLY(i_file_path)

        return None
