#! python3

import System

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper as gh


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
    param = ghenv.Component.Params.Input[indx]    # noqa: F821
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

class DFExportResults(component):
    def __init__(self):
        super(DFExportResults, self).__init__()
        ghenv.Component.ExpireSolution(True)  # noqa: F821
        ghenv.Component.Attributes.PerformLayout()    # noqa: F821
        params = getattr(ghenv.Component.Params, "Input")    # noqa: F821
        for j in range(len(params)):
            X_cord = params[j].Attributes.Pivot.X
            Y_cord = params[j].Attributes.InputGrip.Y
            if params[j].Name == "i_dump":
                add_button(self, "", j, X_cord, Y_cord)

    def RunScript(self, i_dump: bool, i_export_dir: str, i_results):
        if i_dump is None or i_export_dir is None or i_results is None:
            return None

        i_results.dump_pickle(i_export_dir)

        return None
