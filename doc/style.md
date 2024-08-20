(style_guide)=
# Style guide

Here's you can find some documentations and guidelines to contribute to the source code of DF.

---

(git_module)=
## Git

(git_commit_system)=
### GitHub commit convetion
All commits need to be labeled with a tag among these:
```
git commit -m "ADD:<description>"         <--- for adding new elements
git commit -m "FIX:<description>"         <--- for fixing (errors, typos)
git commit -m "FLASH:<description>"       <--- quick checkpoint before refactoring
git commit -m "MILESTONE:<description>"   <--- for capping moment in development
git commit -m "CAP:<description>"         <--- for for less important milestones
git commit -m "UPDATE:<description>"      <--- for moddification to the same file
git commit -m "MISC:<description>"        <--- for any other reasons to be described
git commit -m "WIP:<description>"         <--- for not finished work
git commit -m "REFACTOR:<description>"    <--- for refactored code
git commit -m "MERGE:<description>"       <--- for merging operations
```
You can merge few tags e.g.:
```
git commit -m "WIP-CAP:<description>      <--- for cap moment in not finished work 
```

### Delete submodule
To delete a submodule in Win, you need to:
1. Delete the relevant section from the `.gitmodules` file. The section would look something like this:
```console
[submodule "submodule_name"]
    path = submodule_path
    url = submodule_url
```
2. Stage the `.gitmodules` changes:
```console
git add .gitmodules
```
3. (optional) Delete the relevant section from `.git/config`. The section would look something like this:
```console
[submodule "submodule_name"]
    url = submodule_url
```
4. Run `git rm --cached path_to_submodule` (no trailing slash).
5. Run `Remove-Item -Recurse -Force .git/modules/path_to_submodule`.
6. Commit the changes:
```console
git commit -m "Remove a submodule name"
```

---

(py_conv)=
# Python

## Py sanity check
To ensure the code quality we use the following linter and type checker tools:
- [mypy](https://mypy.readthedocs.io/en/stable/index.html) for type checking.
- [Ruff](https://docs.astral.sh/ruff/) for code quality and style.

(pyghcomp_style)=
## Python Grasshopper Components

Here's the list of convetion for the Grasshopper components for DF in python:
* `i_` for input parameters: e.g. `i_plane` for a plane input.
* `o_` for output parameters: e.g. `o_plane` for a plane output.
* `DF` for the component name: e.g. `DF_tester` for a tester component and the name of the class should be `class DFTester(component)`.

---
(cpp_conv)=
# C++

### Naming & synthax convention
Here's the naming convention for this project:
- ` `: lowerCamelCase.
- `type PublicVariable`: public member of a class
- `type m_PrivateVariable`: Hungarian notation with UpperCamelCase for private class members.
- `static type s_StaticVariable`: Hungarian notation with UpperCamelCase for static members of class.
- `APP_SPEC`: Constants with SNAKE_UPPER_CASE.
- All the other naming uses UpperCamelCase.

Here's an example:
```c++
// do not use using namespace std; we specify the namespace everytime
std::foo()

// next line graph style
void Foo()
{
    /* content */
}

// structure name uses UpperCamelCase
struct AnExampleStruct
{
    // structure attribute uses UpperCamelCase
    const char* Name;
};

// class name uses UpperCamelCase
class AnExampleClass
{
public:
    AnExampleClass(const int& init);
    virtual ~AnExampleClass();

    // member functions use UpperCamelCase
    void PublicMemberFunction()
    {
        // local variable uses lowerCamelCase
        int localVariable = 0;
    }

// A field indicator to separate the functions and attributes
public:
    int PublicVariable;

// Private member function block
private:
    // member functions use UpperCamelCase
    void PrivateMemberFunction(); 

// Also a field indicator to separate the functions and attributes
private:
    // private variables uses Hungarian notation with UpperCamelCase
    int m_PrivateVariable; // m_VariableName for normal variable
    static int s_Instance; // s_VariableName for static variable
};

// Start headers with 
#pragma once

// Start declarations with precompiled headers
#include "aiacpch.h"
```

### Only smart (or unique) pointers
It's 2024, we can pass on raw pointers. We use smart pointers. 
```c++
std::unique_ptr<AnExampleClass> example = std::make_unique<AnExampleClass>(0);
```
Or if you really need to use an unique pointer because you don't want to transfer the ownership of the object, use a shared pointer.
```c++
std::shared_ptr<AnExampleClass> example = std::make_shared<AnExampleClass>(0);
```

### Debugging with GDB
We use GDB for debugging. To install GDB on windows, do the following:
1. Download the MSYS2 installer from the [MSYS2 website](https://www.msys2.org/).
2. Run the installer and follow the instructions in the [MSYS2 installation guide](https://www.msys2.org/wiki/MSYS2-installation/).
3. Open the MSYS2 terminal and update the core package database:
```bash
pacman -Syu
```
4. Install the GDB debugger:
```bash
pacman -S mingw-w64-x86_64-gdb
```
5. Add the GDB to the system path in PATH_ENVIRONMENT:
6. Close the terminal sessions you where using and open a new one. Now you can use GDB.
```bash
gdb "path-to-executable"
```
> use `run` to start the program and `quit` to exit the debugger.
> use `break` to set a breakpoint and `continue` to continue the execution of the program.
> use `bt` to see the backtrace of the program when a segfault occurs.

### Doxygen
For documentation we use the [*JavaDoc" convention](https://doxygen.nl/manual/docblocks.html).
Follow [this guide for documenting the code](https://developer.lsst.io/cpp/api-docs.html).
```c++
/**
 * @brief fill a vector of TSPlanes from a yaml file containing their corners data
 * @param filename path to the map.yaml file
 * @param planes vector of TSPlane objects
 */
```

### Logging
To log use the following MACROS. All the code is contained in `log.hh` and `log.cc`.
```c++
DIFFCHECK_INFO("test_core_info");
DIFFCHECK_WARN("test_core_warn");
DIFFCHECK_ERROR("test_core_error");
DIFFCHECK_FATAL("test_core_critical");
```
The output is like so:
```bash
2024-03-30 12:53:29.971 (   0.000s) [        ADF6D348]        diffCheckApp.cc:24    INFO| test_core_info
2024-03-30 12:53:29.972 (   0.000s) [        ADF6D348]        diffCheckApp.cc:25    WARN| test_core_warn
2024-03-30 12:53:29.972 (   0.000s) [        ADF6D348]        diffCheckApp.cc:26     ERR| test_core_error
2024-03-30 12:53:29.972 (   0.000s) [        ADF6D348]        diffCheckApp.cc:27    FATL| test_core_critical
```
The logging can be silenced by setting ON the option in the main `CMakeLists.txt`.
```cmake
option(SILENT_LOGGING "Do not log messages in the terminal of on." ON)
```

### I/O and basic datatypes
Here's how you can import point cloud from file:
```c++
#include "diffCheck/geometry/DFPointCloud.hh"
#include "diffCheck/geometry/DFMesh.hh"

// clouds
std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr = std::make_shared<diffCheck::geometry::DFPointCloud>();
std::string pathMesh = R"(C:\Users\yourfilecloudpath.ply)";
dfPointCloudPtr->LoadFromPLY(pathCloud);

// mesh
std::shared_ptr<diffCheck::geometry::DFMesh> dfMeshPtr = std::make_shared<diffCheck::geometry::DFMesh>();
std::string pathCloud = R"(C:\Users\yourfilemeshpath.ply)";
dfMeshPtr->LoadFromPLY(pathMesh);
```

### Visualizer

Clouds and mesh can be visualized like this:
```c++
#include "diffCheck/visualizer/DFVisualizer.hh"

// clouds
std::shared_ptr<diffCheck::visualizer::DFVisualizer> dfVisualizerPtr = std::make_shared<diffCheck::visualizer::DFVisualizer>();
dfVisualizerPtr->AddPointCloud(dfPointCloudPtr);
dfVisualizerPtr->Run();

// mesh
std::shared_ptr<diffCheck::visualizer::DFVisualizer> dfVisualizerPtr = std::make_shared<diffCheck::visualizer::DFVisualizer>();
dfVisualizerPtr->AddMesh(dfMeshPtr);
dfVisualizerPtr->Run();
```
