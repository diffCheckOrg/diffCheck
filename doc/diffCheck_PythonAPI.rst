.. currentmodule:: diffCheck

.. _diffCheck_API:

diffCheck Python API
====================

DF's Python API is composed by two main source code directories:

- ``diffCheck``
- ``diffCheck.diffcheck_bindings``

The ``diffCheck`` directory contains the Python API for the DiffCheck's Python API tightly binded to ``RhinoPython``'s modules (``Rhino``, ``rhinoscriptsynthax``, ``scriptcontext`` and ``grasshopper``), while the ``diffCheck.diffcheck_bindings`` directory contains the bindings to the DF's C++ API. In DF we use the ``pybind11`` library to generate the bindings between the C++ and Python APIs and it is reserved to heaevy computational tasks and objects like point clouds, registrations, segmentations, etc.

.. mermaid::
   
      %%{init: {'theme': 'forest'}}%%
      stateDiagram-v2
         direction LR
         diffCheck_C++API --> diffcheck_bindings(pybind11)
         diffcheck_bindings(pybind11) --> RhinoPythonAPI

         state DF_C++API

         state diffcheck_bindings(pybind11)

         state RhinoPythonAPI {
            diffCheck_PythonAPI
         }

.. warning::
   
      The current DF' Python API is not meant to be used as a standalone library. It is meant to be used always in conjuction with `Rhino` and `Grasshopper` ecosystems.
   
Submodules
----------

.. toctree::
   :maxdepth: 1

   diffCheck.df-b_geometries
   diffCheck.df_joint_detector
   diffCheck.df_error_estimation
   diffCheck.df_visualization
   diffCheck.df_cvt_bindings
   diffCheck.df_transformations
   diffCheck.df_util
   
   diffCheck.dfb_registrations
   diffCheck.dfb_segmentation