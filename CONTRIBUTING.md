
# Guide for contributors
Here's you can find some documentations and guidelines to contribute to the source code.

---
# Git

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
```terminal
[submodule "submodule_name"]
    path = submodule_path
    url = submodule_url
```
2. Stage the `.gitmodules` changes:
```terminal
git add .gitmodules
```
3. (optional) Delete the relevant section from `.git/config`. The section would look something like this:
```terminal
[submodule "submodule_name"]
    url = submodule_url
```
4. Run `git rm --cached path_to_submodule` (no trailing slash).
5. Run `Remove-Item -Recurse -Force .git/modules/path_to_submodule`.
6. Commit the changes:
```terminal
git commit -m "Remove a submodule name"
```

---
# Python
DiffCheck is distributed as a Python Grasshopperr plug-in via yak and its source code via PyPI. The plug-in is composed by a series of `.ghuser` components.

There are 3 ways you can contribute to the Python GH plug-in:
1. By adding new components to the plug-in.
2. By fixing bugs of existing components in the plug-in.
3. By adding new functionalities to existing components in the plug-in.

Before committing to the repository you need to have tested the components in the Grasshopper environment and be sure that this is working correctly. Also, provide a sufficient documentation in the PR (for now) please.

Follow these steps to develop and test the Python GH plug-in:
- [GHPy: A) preparation](#ghpy-a-preparation)
- [GHPy: B) development/debug](#ghpy-b-developmentdebug)
- [GHPy: C) Release](#ghpy-c-release)
- [GHPy: D) Documentation](#ghpy-d-documentation)

## GHPy: A) preparation
Download this repo if you haven't already.
```terminal
git clone https://github.com/diffCheckOrg/diffCheck.git
```

Next, if you used diffCheck before as an end-user clean all the `diffCheck folders` in the following directory (the last name will change):
```terminal
C:\Users\<user-name>\.rhinocode\py39-rh8\site-envs\default-wMh5LZL3
```
> note that if you drop an official released diffCheck component from yak, this one will have the `#r : diffCheck==<version_number>` notation at the top of the script. Get rid of all these release components before to start and be sur to erase again the previous folders (they recreated each time `#r : diffCheck` is called).

Build the package from the py source code's directory:
```py
python setup.py sdist bdist_wheel
```

Lastly, install the pip pacakge from the repository in editable mode. This way, all the modifications made to the source code of the repository will be reflected in the installed package. Open a terminal and run the following command (replace the path with where you download the repository):
```terminal
C:\Users\<your-username>\.rhinocode\py39-rh8\python.exe -m pip install -e "<path-to-repository-root>\src\gh\diffCheck"
```

For your info the packages is installed in `C:\Users\andre\.rhinocode\py39-rh8\Lib\site-packages`.

That's it you are now a contributor to the diffCheck! We raccomand to not download anymore from yak package but rather use the source code in the repository. If you want the latest diffCheck, checkout and pull the main.

## GHPy: B) development/debug

### B.1) Code structure
For DiffCheck there are 2 main folders in the repository:
* `src/gh/diffCheck/components` here you can add new components or modify existing ones (for more info on how to create one we point you to [this documentation](https://github.com/compas-dev/compas-actions.ghpython_components)). Here we call the 
* `src/gh/diffCheck/diffCheck` this is our package where the core functionalities are implemented.

### B.2) Developing component's content
The idea is to start by developing the content of the component in the file `src/gh/diffCheck/diffCgeck_app.py`. This would be a simple script that contains the logic of the component. Once the script `diffCheck_app.py` is working correctly, you can move the code to the component file in the `src/gh/diffCheck/components` folder. This is because the component file is the one that will be componentized and distributed via yak.

We reccomand to use `VSCode` as IDE for developing the components. This is because it has a good integration with the `Grasshopper` environment and it is easy to debug the components. To set up the IDE follow these steps:
1. Install the `ScriptSync` extension for `VSCode`.
2. Install the `ScriptSync` from the yak manager in Rhino.
3. Open the `diffCheckApp.py` from the `src/gh/diffCheck/components` folder you are working on in `VSCode`, and set its path to the ScriptSync ghcomponent.
4. If you modify the code in `VSCode`, the changes will be reflected in the Grasshopper component as soon as you save in `VSCode` again the `code.py`.
5. Once your code is working, prepare the code and componentize it.

If you want to use the GHEditor it's ok but everytime you modify the pakcage or the component's code, after any modifications you need to restart the Python interpreter from the ScriptEditor (`Tools > Reload Python3 (CPython) Engine`) and recompute the solution in Grasshopper.

### B.3) Componentize the code
Prepare your component as explained here. You can componentize it locally and test it in Grasshopper. Here's how to componentize:
```terminal
python f:\diffCheck\src\gh\util\componentizer_cpy.py --ghio "C:\Users\andre\.nuget\packages\grasshopper\8.2.23346.13001\lib\net48\" .\src\gh\components\ .\build\gh
```
> Note that you need to find the path to your GHIO folder. This is the folder where the `Grasshopper.dll` is located. E.g. You can find it in the `nuget` folder in the Rhino installation directory.

Once you are sure that the component is working correctly, you can push the changes to the repository.

## GHPy: C) Release
The release will be made via CI from main. As a contributor you don't need to worry about this. The plug-in is componentized, pushed to yak/PyPI and the user can download the latest version from yak.

## GHPy: D) Documentation
More to come.


<!-- ## PyPI
To push the package to PyPI, you need to:
1. Install the package `twine`:
```bash
pip install twine
```
2. Build the package:
```bash
python setup.py sdist bdist_wheel
```
3. Check the package:
```bash
twine check dist/*
```
4. Upload the package:
```bash
twine upload dist/*
```
Be sure to have the right to upload the package to the PyPI repository.
To do so you need to set the `~/.pypirc` file with the following content:
```bash
[distutils]
index-servers=pypi

[pypi]
  username = __token__
  password = pypi-<your-TOKEN>
``` -->

---
# C++

### Naming & synthax convention
Here's the naming convention for this project:
- ` `: lowerCamelCase.
- `type PrivateVariable`: public member of a class
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

<!-- ### Doxygen
For documentation we use the [*JavaDoc" convention](https://doxygen.nl/manual/docblocks.html).
Follow [this guide for documenting the code](https://developer.lsst.io/cpp/api-docs.html).
```c++
/**
 * @brief fill a vector of TSPlanes from a yaml file containing their corners data
 * @param filename path to the map.yaml file
 * @param planes vector of TSPlane objects
 */
``` -->

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


### CTesting (TO BE UPDATED)
When necessary, c++ testing is done by using CTest. Important/critical features (e.g., correcting functioning of graphics with OpenGL and Glfw) needs testing to be written (this is usefull for e.g., GitHub Actions). Such tests can be extracted from the main source code and integrated in a seperate section: cmake testing.

To add a new test do as follow.

First create a new sub-folder in the folder `./test` as `./test/exampletest`.
Here add a console cpp file called `tester.cpp` which returns 0 or 1 and add a new `CMakeLists.txt` as such:
```cmake
add_executable(example_test tester.cpp)

/* <-- 
Insert here linking necessary for the executable
Note that if you already found packages in the head CMakeLists file
you can simply use the macros here.
--> */

add_test(NAME "ExampleTest" COMMAND "example_test" <argv-here> WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}")
```
In the `./test`'s `CMakeLists.txt` add the created sub-directory:
```cmake
if (TEST_EXAMPLE)
    add_subdirectory(exampletest)
endif()
```
Finally add an option in the main `CMakeLists.txt` describing the test:
```cmake
include(CTest)
# ...
option(TEST_EXAMPLE "Test to test something important." ON)
# ...
if(TEST_EXAMPLE)
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/tests/exampletest)
endif()
```

Next, `./configure.sh -c` and `./build.sh` and:
```bash
cd ./build
ctest -N    # <--- to see how many tests there are
ctest -V    # <--- run the tests
```
