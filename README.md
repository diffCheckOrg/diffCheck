<p align="center">
    <img src="./assets/logo/logo_pixelized_bwvioelt.png" width="150">
</p>
<p align="center">
    <img src="https://github.com/diffCheckOrg/diffCheck/actions/workflows/cpp-build.yml/badge.svg">
    <img src="https://github.com/diffCheckOrg/diffCheck/actions/workflows/gh-build.yml/badge.svg">
    <img src="https://github.com/diffCheckOrg/diffCheck/actions/workflows/pypi-build.yml/badge.svg">
    <img href="https://pypi.org/project/diffCheck/" src="https://img.shields.io/pypi/v/diffCheck">
    <img href="https://github.com/ellerbrock/open-source-badges/" src="https://badges.frapsoft.com/os/v2/open-source.svg?v=103">
</p>



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

```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title       diffCheck - backend dev
    excludes    weekends

    data i/o                                 :active, dataio, 2024-03-15, 3w
    global registration                      :glbreg, 2024-03-29, 2w
    semantic seg. from 3D model              :semseg, after glbreg, 1w
    local registration                       :locreg, after semseg, 2w
    error computation + results              :errcomp, after locreg, 1w
```

## 3rd party libraries

The project uses the following 3rd party libraries:
- `Open3d 0.18.0` for 3D point cloud processing as pre-build binaries ([store here](https://github.com/diffCheckOrg/submodule-open3d.git))
- `Eigen` for linear algebra
- `CGAL` for general geometric processing and IO
- `Boost` for general utilities as pre-build binaries ([store here](https://github.com/diffCheckOrg/submodule-boost.git))

## How to build c++ project
To build and test the project, follow the following steps:

```terminal
cmake/config.bat
cmake/build.bat
./build/bin/Release/diffCheckApp.exe <-- for prototyping
```

## Prototype diffCheck in C++
To prototype:
1) add a header/source file in `src/diffCheck` and include the header in `diffCheck.hh` interface
1) test it in `diffCheckApp` (the cmake will output an executable in bin)

See the [CONTRIBUTING.md](https://github.com/diffCheckOrg/diffCheck/blob/main/CONTRIBUTING.md) for more information on how to prototype with diffCheck (code guidelines, visualizer, utilities, etc).

