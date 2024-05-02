# diffCheck
<p align="left">
    <img src="https://github.com/diffCheckOrg/diffCheck/actions/workflows/win-build.yml/badge.svg">
</p>

Temporary repository for diffCheck

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
- `Open3d 0.18.0` for 3D point cloud processing as pre-build binaries)
- `Eigen` for linear algebra
- `CGAL` for general geometric processing and IO
- `Boost` for general utilities as pre-build binaries

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


## TODO:
- [ ] @Andrea: add writing functions for mesh and point cloud
- [ ] @Andrea: refactor `IOManager.hh` with a class `IOManager` and static methods
- [ ] @Andrea: test Rhino exporeted `.ply` files
- [ ] @Andrea: tests suite for IO /pcdmesh / visualizer
