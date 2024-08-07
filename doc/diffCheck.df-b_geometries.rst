.. _diffCheck-df-b_geometries:

``diffCheck.df-b_geometries`` modules
=====================================

This page contains 2 modules for the geometries:

1. :mod:`diffCheck.df_geometries` module contains all the objects and functions to handle geometries of a structure in the DiffCheck library.
2. :mod:`diffCheck.diffcheck_bindings.dfb_geometry` module contains all the objects and functions to handle mesh and point cloud geometries in diffCheck.


.. _diffCheck-df_geometries:

``diffCheck.df_geometries`` module
==================================
.. currentmodule:: diffCheck.df_geometries

This module represent the geometry of a structure in the DiffCheck library. It contains the following classes:

- :class:`diffCheck.df_geometries.DFAssembly`
- :class:`diffCheck.df_geometries.DFBeam`
- :class:`diffCheck.df_geometries.DFJoint`
- :class:`diffCheck.df_geometries.DFFace`
- :class:`diffCheck.df_geometries.DFVertex`

This is how these geometris are related:

.. mermaid::

   stateDiagram-v2
    DFAssembly
      state DFAssembly {

         [*] --> DFBeam
         state DFBeam {

            [*] --> DFJoint
            DFJoint --> DFFace

            state DFFace {
               [*] --> DFVertex
            }
         }
      }

.. caution::
   
      The :class:`diffCheck.df_geometries.DFJoint` is only generated when accessed from the :class:`diffCheck.df_geometries.DFAssembly` or :class:`diffCheck.df_geometries.DFBeam` objects. It exists only as a convinience container for the joints.

.. automodule:: diffCheck.df_geometries
   :members:
   :undoc-members:
   :show-inheritance:

``diffCheck.diffcheck_bindings.dfb_geometry`` module
====================================================
.. currentmodule:: diffCheck.diffcheck_bindings.dfb_geometry

.. automodule:: diffCheck.diffcheck_bindings.dfb_geometry
   :members:
   :undoc-members:
   :show-inheritance: