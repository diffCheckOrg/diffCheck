<p align="center">
    <img src="./logo.png" width="150">
</p>
<p align="center">
    <img src="https://github.com/diffCheckOrg/diffCheck/actions/workflows/cpp-build.yml/badge.svg">
    <img src="https://github.com/diffCheckOrg/diffCheck/actions/workflows/test-pass.yml/badge.svg">
    <img src="https://github.com/diffCheckOrg/diffCheck/actions/workflows/gh-build.yml/badge.svg">
    <img src="https://github.com/diffCheckOrg/diffCheck/actions/workflows/pypi-build.yml/badge.svg">
    <img src="https://github.com/diffCheckOrg/diffCheck/actions/workflows/doc-build.yml/badge.svg">
    <img src="https://github.com/diffCheckOrg/diffCheck/actions/workflows/yak-build.yml/badge.svg">
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/diffCheck?style=flat&logo=pypi&logoColor=white&color=blue">
    <img alt="Dynamic JSON Badge" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fyak.rhino3d.com%2Fpackages%2FdiffCheck&query=%24.version&logo=rhinoceros&label=Yak&color=%23a3d6ff">
    <a href="https://doi.org/10.5281/zenodo.13843959"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.13843959.svg" alt="DOI"></a>
</p>


![demo](https://github.com/user-attachments/assets/3c9f353d-7707-4630-aa6d-fe59cbdeae2f)

# DiffCheck: CAD-Scan comparison

With `diffCheck`, you can easily compare your scans and 3D models of timber structures or joinery to measure precision and see the differences at a glance, [here](https://diffcheckorg.github.io/diffCheck/quickstart.html)!

`diffCheck` can also function as a general purpose  point cloud processing toolset and we hope that the digital community will use it, see the interest, and contribute to this open-source project we starting!

`diffCheck` is originally developed and now maintained by Andrea Settimi (PhD), Damien Gilliard (PhD) from the [Laboratory of Timber Construction (IBOIS, lab head: Prof. Yves Weinand)](https://www.epfl.ch/labs/ibois/), Eleni Skevaki (PhD) and Dr. Marirena Kladeftira (Post-Doc) from the [Laboratory for Creative Computation (CRCL, lab head: Prof. Stefana Parascho)](https://www.epfl.ch/labs/crcl/) here at [Ecole Polytechnique Fédérale de Lausanne (EPFL)](https://www.epfl.ch/en/).

`diffCheck` is designed to be user-friendly and can be used either via a Grasshopper plug-in, we provide tutorials and online documentation for each component and its Python API.

## Quickstart

The main interface is a Grasshopper plug-in, it's distributed via the yak package manager so just type the `_PackageManager` in Rhino and type 

```
diffCheck
```

Open your Grasshopper canvas and search for the `DF` components!

## Functionalities

`diffCheck` is a toolset that allows you to compare a 3D model of a structure to evaluate its assembly or joint's quality and accuracy.

<div align="center">
    <img src="./assets/img/placeholder_additive.png" width="600">
    <p>Example of several structures assembled with different digital technologies.</p>
</div>
<div align="center">
    <img src="./assets/img/placeholder_subtractive.png" width="600">
    <p>Example of joinery evaluation.</p>
</div>


## Documentation

The full documentation, with tutorials, automatic documentation for GHComponents and PythonAPI is available [here](https://diffcheckorg.github.io/diffCheck/).



## Roadmap

```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title       diffCheck - general overview
    excludes    weekends

    section Workshop
    Workshop dryrun                         :milestone, crit, dryrun, 2025-09-15, 1d
    Workshop in Boston                      :workshop, 2025-11-16, 2d

    section Component development
    Pose estimation                         :CD1, 2025-05-15, 1w
    Communication w/ hardware               :CD2, after CD1, 3w
    Pose comparison                         :CD3, after CD1, 3w
    General PC manipulation                 :CD4, after CD1, 6w
    Data analysis component                 :CD5, after CD3, 3w

    section Workshop preparation
    Workshop scenario                       :doc1, 2025-08-01, 1w
    New compilation documentation           :doc2, after mac, 2w
    New components documentation            :doc2, 2025-08-01, 4w
    Development of special pipeline for data:doc3, after doc1, 3w

    section Cross-platform
    adaptation of CMake for mac compilation :mac, 2025-07-01, 3w

    section Prototype testing
    Fabrication of iterative prototype      :fab, 2025-08-01, 2w
```

## How to contribute

If you want to contribute to the project, please refer to the [contribution guidelines]([./CONTRIBUTING.md](https://diffcheckorg.github.io/diffCheck/contribute.html)).
