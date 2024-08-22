
.. _test_guide:

DFTesting
=========

Ideally, if we add code to the project, we should also add tests (at least unit tests).
In df we use `CTest` as a test framework managed by Cmake in the file ``cmake/tests.cmake`` to run:

* `c++ <#cpp_test>`_ tests with `GoogleTest`, and
* `Python <#py_test>`_ in `PyTest`.

Tests are in the ``tests`` folder, and here's its structure:

.. code-block:: console

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

To run the tests, you can use the following commands:

.. code-block:: console

   cmake -S . -B build -A x64 -DBUILD_PYTHON_MODULE=ON -DBUILD_TESTS=ON -DRUN_TESTS=ON
   cmake --build build --config Release


.. _py_test:

Write DF Python tests
---------------------

To write a test, you need to create a new file in the ``tests/integration_tests`` folder. Write a new ``.py`` test file if you are not contributing to an already existing test, and add it in the ``cmake/tests.cmake`` in the ``add_test()`` function:

.. code-block:: cmake

   add_test(NAME PYBIND_UNIT_TEST 
            COMMAND ${PYTHON_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/tests/integration_tests/pybinds_tests/test_pybind_units.py 
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} 
            )

Use a fixture to your needs, and write your test. Here is an example of a fixture that always load a point cloud from the ``test_data`` folder:

.. literalinclude:: ../tests/integration_tests/pybinds_tests/test_pybind_units.py
   :language: python
   :pyobject: create_DFPointCloudSampleRoof
   :caption: `test_pybind_units.py <../tests/integration_tests/pybinds_tests/test_pybind_units.py>`_

Than you can use it in your test:

.. literalinclude:: ../tests/integration_tests/pybinds_tests/test_pybind_units.py
        :language: python
        :pyobject: test_DFPointCloud_apply_color


.. _cpp_test:

Write DF C++ tests
------------------

To write a test, you need to create a new file in the ``tests/unit_tests`` folder. Next add your file in the executable ``${CPP_UNIT_TESTS}`` in the ``cmake/tests.cmake``:

.. code-block:: cmake

   add_test(NAME PYBIND_UNIT_TEST 
         COMMAND ${PYTHON_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/tests/integration_tests/pybinds_tests/test_pybind_units.py 
         WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} 
         )

Use a fixture to your needs, and write your test. Here is an example of a fixture that always load a point cloud from the ``test_data`` folder:

.. literalinclude:: ../tests/unit_tests/DFPointCloudTest.cc
        :language: cpp
        :lines: 1-27
        :caption: `DFPointCloudTest.cc <../tests/unit_tests/DFPointCloudTest.cc>`_

and you can use it in your test:

.. code-block:: cpp

        TEST_F(DFPointCloudTestFixture, HasColors) {
                EXPECT_TRUE(dfPointCloud.HasColors());
        }