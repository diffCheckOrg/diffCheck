#! python3


from ghpythonlib.componentbase import executingcomponent as component

from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import diffCheck
import diffCheck.df_cvt_bindings
from diffCheck import diffcheck_bindings

class DFTester(component):
    def RunScript(self):
        # version
        ghenv.Component.Message = f"diffCheck v: {diffCheck.__version__}"  # noqa: F821

        # bindings
        is_binding_imported = diffcheck_bindings.dfb_test.test()
        if not is_binding_imported:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Bindings not imported.")  # noqa: F821
        else:
            ghenv.Component.AddRuntimeMessage(RML.Remark, "Bindings imported.")  # noqa: F821
        print(f"diffCheck test: {diffCheck.df_cvt_bindings.test_bindings()}")

        # workspace unit
        scalef = diffCheck.df_util.get_doc_2_meters_unitf()
        if scalef != 1.0:
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Workspace unit is not in meters.")  # noqa: F821
        else:
            ghenv.Component.AddRuntimeMessage(RML.Remark, "Workspace unit is in meters.")  # noqa: F821

        return is_binding_imported
