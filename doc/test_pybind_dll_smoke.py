""" This file contains a simple test for the Python bindings to the C++ code (dlls reading, pyd importing etc). """

import pytest
import os
import sys

# Import the C++ bindings
extra_dll_dir = os.path.abspath(os.path.dirname(__file__))
print(f"extra_dll_dir: {extra_dll_dir}")
sys.path.append(extra_dll_dir)  # Add this directory to the Python path
# os.add_dll_directory(extra_dll_dir)  # For finding DLL dependencies on Windows
try:
    import diffCheck.diffcheck_bindings as dfb
except ImportError as e:
    print(f"Failed to import diffcheck_bindings: {e}")
    print("Current sys.path directories:")
    for path in sys.path:
        print(path)
    print("Current files in the directory:")
    for file in os.listdir(extra_dll_dir):
        print(file)
    sys.exit(1)

# def test_dfb_test_simple():
#     assert dfb.dfb_test.test() == True, "The test function should return True"

# if __name__ == "__main__":
#     pytest.main()
print(">>>>>>>>>>>>>>>>> test_pybind_dll_smoke.py succeded <<<<<<<<<<<<<<<<<<<<")