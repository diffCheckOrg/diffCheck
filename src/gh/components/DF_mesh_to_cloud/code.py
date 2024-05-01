#! python3

import System
import typing

import Rhino
import Rhino.Geometry as rg
from ghpythonlib.componentbase import executingcomponent as component

import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
from diffCheck import diffcheck_bindings.dfb_geometry

class DFMeshToCloud(component):
    def RunScript(self,
            i_mesh: rg.Mesh):
        """
            Convert a Rhino mesh to a cloud.

            :param i_mesh: mesh to convert

            :return o_cloud: rhino cloud
        """

        return True



        # is_binding_imported = diffCheckBindings.test()

        # if not is_binding_imported:
        #     ghenv.Component.AddRuntimeMessage(RML.Warning, "Bindings not imported.")
        # else:
        #     ghenv.Component.AddRuntimeMessage(RML.Remark, "Bindings imported.")

        # return is_binding_imported

###################################################################
# >>>>>>>> DEBUG START - to comment out when componentized >>>>>>>>
###################################################################

if __name__ == "__main__":
    comp = DFMeshToCloud()
    o_is_imported = comp.RunScript(i_mesh)