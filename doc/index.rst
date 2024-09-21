.. _diffcheck_intro:

DiffCheck: CAD-Scan comparison
=====================================

diffCheck(DF) allows to *identify discrepancies across point clouds and 3D models of both individually machined timber pieces featuring various joints as well as fully assembled timber structures*. It can help you quantify the differences between the CAD and scanned fabricated structure, providing a comprehensive report that highlights the discrepancies.

The software is designed to be user-friendly and can be used either via a Grasshopper plug-in or its Python API.

The software is developed by the `Laboratory of Timber Construction (IBOIS)`_ and the `Laboratory for Creative Computation (CRCL)`_ at `Polytechnique Fédérale de Lausanne (EPFL)`_.

.. raw:: html

   <div style="text-align: center;">
       <img src="_static/front_bothroundsquare.png" alt="diffCheck Front Image" style="background-color: transparent; width: 100%; max-width: 800px;">
   </div>

.. grid:: 3
   :margin: 0
   :padding: 0
   :gutter: 0

   .. grid-item-card:: Grasshoper plug-in
      :columns: 12 6 6 4
      :class-card: sd-border-0
      :shadow: None

      diffCheck is distributed as a Grasshopper plug-in, allowing users to easily compare CAD models with scanned point clouds comfortably within the Rhino environment.

   .. grid-item-card:: GH documentation
      :columns: 12 6 6 4
      :class-card: sd-border-0
      :shadow: None

      We provide detailed documentation on how to use the software, including installation instructions, tutorials, and components descriptions.

   .. grid-item-card:: Developer resources
      :columns: 12 6 6 4
      :class-card: sd-border-0
      :shadow: None

      diffCheck is also available as a Python API, allowing developers to integrate the software into their own workflows within the Rhino ecosystem. We also welcome contributions to the project!

.. grid:: 3

    .. grid-item-card::
      :columns: 12 6 6 4
      :class-card: sd-border-0
      :shadow: None

      .. button-ref:: qstart
        :expand:
        :ref-type: myst
        :color: success
        :click-parent:

        :octicon:`zap;2em` Get start!

    .. grid-item-card::
      :columns: 12 6 6 4
      :class-card: sd-border-0
      :shadow: None

      .. button-ref:: gh_dfcomp
        :expand:
        :ref-type: myst
        :color: success
        :click-parent:

        :octicon:`book;2em` GHComponents

    .. grid-item-card::
      :columns: 12 6 6 4
      :class-card: sd-border-0
      :shadow: None

      .. button-ref:: dev_df_doc
        :expand:
        :ref-type: myst
        :color: success
        :click-parent:

        :octicon:`codespaces;2em` To the Dev docs

.. grid:: 3
   :margin: 0
   :padding: 0
   :gutter: 0

   .. grid-item-card:: Tutorials
      :columns: 12 6 6 4
      :class-card: sd-border-0
      :shadow: None

      We provide a series of hands-on tutorials to help you get started with diffCheck. The tutorials are based on real timber structures and will guide you through the process of comparing CAD models with scanned point clouds.

   .. grid-item-card:: Python API
      :columns: 12 6 6 4
      :class-card: sd-border-0
      :shadow: None

      If you prefer to work with Python, you can use diffCheck's Python API for Rhino. The API allows you to access the software's functionality directly from your Python scripts.

   .. grid-item-card:: Open-source
      :columns: 12 6 6 4
      :class-card: sd-border-0
      :shadow: None

      diffCheck is an open-source project, and we welcome contributions from the community. If you have ideas for new features or improvements, feel free to get in touch!

.. grid:: 3

    .. grid-item-card::
      :columns: 12 6 6 4
      :class-card: sd-border-0
      :shadow: None

      .. button-ref:: df-tuto
        :expand:
        :ref-type: myst
        :color: success
        :click-parent:

        :octicon:`beaker;2em` Learn diffCheck

    .. grid-item-card::
      :columns: 12 6 6 4
      :class-card: sd-border-0
      :shadow: None

      .. button-ref:: diffCheck_API
        :expand:
        :ref-type: myst
        :color: success
        :click-parent:

        :octicon:`terminal;2em` DF in Python

    .. grid-item-card::
      :columns: 12 6 6 4
      :class-card: sd-border-0
      :shadow: None

      .. button-ref:: contrib_guide
        :expand:
        :ref-type: myst
        :color: success
        :click-parent:

        :octicon:`heart;2em` Contribute

.. toctree::
    :hidden:
    :maxdepth: 2
    :caption: Getting Started

    installation
    quickstart
    tutorials

    gh_components


.. toctree::
    :hidden:
    :maxdepth: 3
    :caption: Further resources

    df_architecture
    diffCheck_PythonAPI
    dev_documentation
    glossary


.. _Laboratory of Timber Construction (IBOIS): https://www.epfl.ch/labs/ibois/
.. _Laboratory for Creative Computation (CRCL): https://www.epfl.ch/labs/crcl/
.. _Polytechnique Fédérale de Lausanne (EPFL) : https://www.epfl.ch/en/