import os
import sys

__version__ = "1.3.0"

if not os.getenv('SPHINX_BUILD', False):
    # For windows:
    if os.name == 'nt':
        # make the dlls available to the python interpreter
        PATH_TO_DLL = "dlls"
        extra_dll_dir = os.path.join(os.path.dirname(__file__), PATH_TO_DLL)
        os.add_dll_directory(extra_dll_dir)
        # from . import diffcheck_bindings  # type: ignore[attr-defined]

    # # For macos:
    # if os.name == 'posix':
    #     # append so files to the python path
    #     PATH_TO_SO = "so"
    #     extra_so_dir = os.path.join(os.path.dirname(__file__), PATH_TO_SO)
    #     sys.path.append(extra_so_dir)
    
    # import diffcheck_bindings  # type: ignore[attr-defined]
    # from .so.diffcheck_bindings import *
    from . import df_cvt_bindings  # type: ignore[attr-defined]
