#! python3

import System

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
from diffCheck import diffCheckBindings

class DFMeshToCloud(component):
    def RunScript(self):
        """
            The component test and import bind module for diffCheck.
        """
        ghenv.Component.Message = f"diffCheck v: {diffCheck.__version__}"
        is_binding_imported = diffCheckBindings.test()

        if not is_binding_imported:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Bindings not imported.")
        else:
            ghenv.Component.AddRuntimeMessage(RML.Remark, "Bindings imported.")

        return is_binding_imported

###################################################################
# >>>>>>>> DEBUG START - to comment out when componentized >>>>>>>>
###################################################################

if __name__ == "__main__":
    comp = DFMeshToCloud()
    o_is_imported = comp.RunScript()