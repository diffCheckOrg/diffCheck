
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

### Logging (TO BE UPDATED)
To log use the following MACROS. All the code is contained in `Log.hpp` and `Log.cpp`. 
```c++
AIAC_INFO("test_core_info");
AIAC_WARN("test_core_warn");
AIAC_CRITICAL("test_core_critical");
AIAC_DEBUG("test_core_debug");
AIAC_ERROR("test_core_error");
```
The output is like so:
```bash
[source main.cpp] [function main] [line 32] [16:30:05] APP: test
```
The logging can be silenced by setting OFF the option in the main `CMakeLists.txt` and do clean reconfiguration.
```cmake
option(SILENT_LOGGING "Do not log messages in the terminal of on." ON)
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
