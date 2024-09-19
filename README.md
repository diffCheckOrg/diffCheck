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
</p>


# DiffCheck: CAD-Scan comparison

diffCheck(DF) allows to identify discrepancies across point clouds and 3D models of both individually machined timber pieces featuring various joints as well as fully assembled timber structures. It can help you quantify the differences between the CAD and scanned fabricated structure, providing a comprehensive report that highlights the discrepancies.

The software is designed to be user-friendly and can be used either via a Grasshopper plug-in or its Python API.

Visit the [DiffCheck website](https://diffcheckorg.github.io/diffCheck/) for more information and documentation.

![demo](https://github.com/user-attachments/assets/3c9f353d-7707-4630-aa6d-fe59cbdeae2f)

The software is developed by the [Laboratory of Timber Construction (IBOIS)](https://www.epfl.ch/labs/ibois/) and the [Laboratory for Creative Computation (CRCL)](https://www.epfl.ch/labs/crcl/) at [Polytechnique Fédérale de Lausanne (EPFL)](https://www.epfl.ch/en/).


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
