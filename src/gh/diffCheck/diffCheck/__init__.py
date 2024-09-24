import os

__version__ = "0.0.41"

# make the dlls available to the python interpreter
PATH_TO_DLL = "dlls"
extra_dll_dir = os.path.join(os.path.dirname(__file__), PATH_TO_DLL)
os.add_dll_directory(extra_dll_dir)

if not os.getenv('SPHINX_BUILD', False):
    from . import diffcheck_bindings  # type: ignore[attr-defined]
    from . import df_cvt_bindings  # type: ignore[attr-defined]
    from . import df_util  # type: ignore[attr-defined]
    from . import df_joint_detector  # type: ignore[attr-defined]
    from . import df_geometry  # type: ignore[attr-defined]
    from . import df_transformations  # type: ignore[attr-defined]
    from . import df_error_estimation  # type: ignore[attr-defined]
    from . import df_visualization  # type: ignore[attr-defined]
