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


![demo](./assets/img/intro_illustration_with_final_distances_and_pose_estimation.png)

# DiffCheck: CAD-Scan comparison

With `diffCheck`, you can easily compare your scans and 3D models of timber structures or joinery to measure precision and see the differences at a glance, [here](https://diffcheckorg.github.io/diffCheck/quickstart.html)!

`diffCheck` can also function as a general purpose  point cloud processing toolset and we hope that the digital community will use it, see the interest, and contribute to this open-source project we starting!

`diffCheck` 1 was originally developed by Dr. Andrea Settimi, Damien Gilliard (PhD candidate) from the [Laboratory of Timber Construction (IBOIS, lab head: Prof. Yves Weinand)](https://www.epfl.ch/labs/ibois/), Eleni Skevaki (PhD candidate) and Dr. Marirena Kladeftira (Post-Doc) from the [Laboratory for Creative Computation (CRCL, lab head: Prof. Stefana Parascho)](https://www.epfl.ch/labs/crcl/) here at [Ecole Polytechnique Fédérale de Lausanne (EPFL)](https://www.epfl.ch/en/). Development for the version 2 was done by Damien Gilliard (still PhD candidate) from the [Laboratory of Timber Construction (IBOIS, lab head: Prof. Yves Weinand)](https://www.epfl.ch/labs/ibois/) and Eleni Skevaki (PhD candidate) from the [Laboratory for Creative Computation (CRCL, lab head: Prof. Stefana Parascho)](https://www.epfl.ch/labs/crcl/).

`diffCheck` is designed to be user-friendly and can be used either via a Grasshopper plug-in, we provide tutorials and online documentation for each component and its Python API.

## Quickstart

The main interface is a Grasshopper plug-in, it's distributed via the yak package manager so just type the `_PackageManager` in Rhino and type 

```
diffCheck
```

Open your Grasshopper canvas and search for the `DF` components!

## Functionalities

`diffCheck` is a toolset that allows you to compare a 3D model of a structure to evaluate its assembly or joint's quality and accuracy. It can be used on finished assemblies to evaluate their quality, but also to detect poses during fabrication, to allow fabricator to react to pose discrepancies on-the-fly.

<div align="center">
    <img src="./assets/img/placeholder_additive.png" width="600">
    <p>Example of several finished structures assembled with different digital technologies.</p>
</div>
<div align="center">
    <img src="./assets/img/placeholder_subtractive.png" width="600">
    <p>Example of joinery evaluation.</p>
</div>
<div align="center">
    <img src="./assets/img/pose_detection.png" width="400">
    <p>Example of pose estimation.</p>
</div>

## Documentation

The full documentation, with tutorials, automatic documentation for GHComponents and PythonAPI is available [here](https://diffcheckorg.github.io/diffCheck/).


## How to contribute

If you want to contribute to the project, please refer to the [contribution guidelines]([./CONTRIBUTING.md](https://diffcheckorg.github.io/diffCheck/contribute.html)).

