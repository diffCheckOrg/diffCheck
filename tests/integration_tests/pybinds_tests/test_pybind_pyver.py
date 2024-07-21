from __future__ import absolute_import, print_function
import pefile
import os
import sys
import re
sys.path.append('./pefile_py3-master')

print("python env: v.%s.%s" % (sys.version_info.major, sys.version_info.minor))
print("pefile lib: v.%s" % pefile.__version__)

dll_path = os.path.join(os.path.dirname(__file__), 'diffcheck_bindings.cp39-win_amd64.pyd')
print("path to pyd: %s" % dll_path)
dll_py_ver = ""

pe = pefile.PE(dll_path)
if pe.is_dll():
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        if b"python" in entry.dll:
            dll_name = entry.dll.decode('utf-8')
            # Assuming the DLL name follows the pattern "pythonXY.dll"
            # where X is the major version and Y is the minor version.
            version_match = re.search(r'python(\d)(\d)\.dll', dll_name)
            if version_match:
                major_version = version_match.group(1)
                minor_version = version_match.group(2)
                version = f"{major_version}.{minor_version}"
                if pe.FILE_HEADER.Machine == 0x14C:
                    arch = "x86"
                elif pe.FILE_HEADER.Machine == 0x8664:
                    arch = "x64"
                else:
                    arch = "unknown"
                print(f">>> importing {dll_name}: v.{version} [{arch}] <<<")
                dll_py_ver = version
else:
    print("not a DLL file")

print("pybind DLL python version: %s" % dll_py_ver)