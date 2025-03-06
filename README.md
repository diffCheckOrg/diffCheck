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

## New Goals (copied from slack)

1. Test with different hardware and scans
2. Bring in more case studies
3. Clear roadmap and futures list for someone to contribute
4. import general pcd processing tools (coackroach)
5. New dev axe on live benchmarking
6. component with a web socket reading PCD batches. (GitHub - behrooz-tahanzadeh/Bengesht: A collection of components for Grasshopper3D)
7. Error diagnosis (example displacement direction compared to face)
8. Add ai-based segmentation methods

## Roadmap

```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title       diffCheck - general overview
    excludes    weekends

    section Publication
    Abstract edition                    :active, absed, 2024-03-01, 2024-03-15
    Submission abstract ICSA            :milestone, icsaabs, 2024-03-15, 0d
    Paper edition                       :paperd, 2024-10-01, 2024-10-30
    Submission paper ICSA               :milestone, icsapap, 2024-10-30, 0d

    section Code development
    Backend development                 :backenddev, after icsaabs, 6w
    Rhino/Grasshopper integration       :rhghinteg, after backenddev, 6w
    Documentation & Interface           :docuint, after fabar, 3w

    section Prototype testing
    Fabrication of AR Prototype         :crit, fabar, 2024-07-01, 2024-08-30
    Fabrication of CNC Prototype        :crit, fabcnc, 2024-07-01, 2024-08-30
    Fabrication of Robot Prototype      :crit, fabrob, 2024-07-01, 2024-08-30
    Data collection and evaluation      :dataeval, after fabrob, 4w
```

## How to contribute

If you want to contribute to the project, please refer to the [contribution guidelines]([./CONTRIBUTING.md](https://diffcheckorg.github.io/diffCheck/contribute.html)).
