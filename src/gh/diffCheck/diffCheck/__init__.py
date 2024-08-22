import os

__version__ = "0.0.24"

# make the dlls available to the python interpreter
PATH_TO_DLL = "dlls"
extra_dll_dir = os.path.join(os.path.dirname(__file__), PATH_TO_DLL)
os.add_dll_directory(extra_dll_dir)

# import the bindings
from . import diffcheck_bindings
