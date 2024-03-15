
# Guide for contributors
Here's you can find some documentations and guidelines to contribute to the source code.

#==============================================================
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

#==============================================================
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


### Pre-Compiled headers
AC uses a precompile header `aiacpch.h` to the project to shorten compilation time for headers that you rarely modify such as stdb library, opencv etc.. Add to `aiacpch.h` every big header you do not use often.
Include at the very top `#include "aiacpch.h"` of every `.cpp` file.


### Logging
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

### CTesting
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
