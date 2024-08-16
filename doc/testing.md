(test_guide)=
# Test guide

In df we use `CTest` as a test framework managed by Cmake in the file `cmake/tests.cmake` to run:
* [c++](cpp_test) tests with `GoogleTest`, and
* [python](py_test) in `PyTest`.

Tests are in the `tests` folder, and here's its structure:
```terminal
F:\DIFFCHECK\TESTS
│   allCppTests.cc
│
├───integration_tests  <-- mainly python interfaces
│   ├───ghcomponents_tests   <-- relative to gh components
│   │       .gitkeep
│   │
│   ├───package_tests  <-- relative to the pypi package
│   │       .gitkeep
│   │
│   └───pybinds_tests  <-- strictly pybinding
│       │   diffCheck.dll
│       │   diffcheck_bindings.cp39-win_amd64.pyd
│       │   Open3D.dll
│       │   test_pybind_pyver.py
│       │   test_pybind_units.py
│
├───test_data  <-- here is where we put some .ply data
│       roof_quarter.ply
│
└───unit_tests  <-- c++ backend, one for each header
        DFLog.cc
        DFPointCloudTest.cc
```

To run the tests, you can use the following commands:
```terminal
cmake -S . -B build -A x64 -DBUILD_PYTHON_MODULE=ON -DBUILD_TESTS=ON -DRUN_TESTS=ON
cmake --build build --config Release
```

(py_test)=
## Write Python tests

To write a test, you need to create a new file in the `tests/integration_tests` folder. Write a new `.py` test file and add it in the `cmake/tests.cmake` in the `add_test` function.
e.g.:
https://github.com/diffCheckOrg/diffCheck/blob/e080a93cdd73d96efb0686f80bf13730e0b8efa3/cmake/tests.cmake#L45-L48


(cpp_test)=
## Write C++ tests

To write a test, you need to create a new file in the `tests/unit_tests` folder. Next add your file in the executable `${CPP_UNIT_TESTS}` in the `cmake/tests.cmake`.
e.g.:
https://github.com/diffCheckOrg/diffCheck/blob/e080a93cdd73d96efb0686f80bf13730e0b8efa3/cmake/tests.cmake#L13-L17