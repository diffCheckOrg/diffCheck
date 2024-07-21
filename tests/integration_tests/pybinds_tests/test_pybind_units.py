import pytest
import os
import sys

# Setup for importing the .pyd module
PATH_TO_DLL = "dlls"
extra_dll_dir = os.path.join(os.path.dirname(__file__), PATH_TO_DLL)
os.add_dll_directory(extra_dll_dir)  # For finding DLL dependencies on Windows
sys.path.append(extra_dll_dir)  # Add this directory to the Python path
try:
    import diffcheck_bindings
except ImportError as e:
    print(f"Failed to import diffcheck_bindings: {e}")
    # Optionally, list the directories in sys.path for debugging
    print("Current sys.path directories:")
    for path in sys.path:
        print(path)
    sys.exit(1)

# FIXME: do real dfbindings unit tests
def test_addition():
    result = 2 + 1
    assert result == 3, "Expected addition result to be 3"

if __name__ == "__main__":
    pytest.main()