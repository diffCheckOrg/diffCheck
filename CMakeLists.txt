cmake_minimum_required(VERSION 3.16.)
project(diffCheck VERSION 1.3.1 LANGUAGES CXX C)
set(CMAKE_CXX_STANDARD 17)

list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

include(external_tools)
include(options)

# disabling warnings
if (MSVC)
    add_compile_options(/wd4003)
endif()

# check that the -DCMAKE_BUILD_TYPE is set
if(NOT CMAKE_BUILD_TYPE)
    message(STATUS "Setting build type to 'Release' as none was specified.")
    set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build." FORCE)
endif()

# do a submodule init if not done already
execute_process(COMMAND git submodule update --init --recursive
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    RESULT_VARIABLE GIT_SUBMOD_RESULT
    )
if(NOT GIT_SUBMOD_RESULT EQUAL "0")
    message(FATAL_ERROR "git submodule update --init --recursive failed with ${GIT_SUBMOD_RESULT}, please checkout submodules")
endif()

#--------------------------------------------------------------------------
# pre-compiled definitions
#--------------------------------------------------------------------------
if(SILENT_LOGGING)
    target_compile_definitions(${PROJECT_NAME} PRIVATE SILENT_LOGGING=true)
endif()

#--------------------------------------------------------------------------
# diffCheck dynamic lib
#--------------------------------------------------------------------------
set(SHARED_LIB_NAME diffCheck)

file(GLOB_RECURSE SOURCES_LIB 
    src/diffCheck.hh                         # diffCheck interface
    src/diffCheck/*.cc src/diffCheck/*.hh    # diffCheck src  
    )

add_library(${SHARED_LIB_NAME} SHARED ${SOURCES_LIB})

if (WIN32)
    set_target_properties(${SHARED_LIB_NAME} PROPERTIES
        WINDOWS_EXPORT_ALL_SYMBOLS TRUE
        )
endif()
    set_target_properties(${SHARED_LIB_NAME} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin  # for dll
        ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib  # for lib
        )
target_include_directories(${SHARED_LIB_NAME}
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src
    )

#set the MD_DynamicRelease flag for MSVC since we are compiling with /MD for py wrap
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")


#--------------------------------------------------------------------------
# 3rd party
#--------------------------------------------------------------------------

# Eigen -------------------------------------------------------------------
download_submodule_project(eigen)
add_subdirectory(deps/eigen)
target_link_libraries(${SHARED_LIB_NAME} PUBLIC Eigen3::Eigen)

# Open3D (pre-built binaries) ---------------------------------------------
download_submodule_project(open3d)
set(Open3D_DIR ${CMAKE_CURRENT_SOURCE_DIR}/deps/open3d/win/0_18/CMake)
find_package(Open3D 0.18.0 REQUIRED)

# print the version debug or release of the package
message(STATUS "Open3D version: ${Open3D_VERSION}"
               "Open3D include dir: ${Open3D_INCLUDE_DIRS}"
               "Open3D library dir: ${Open3D_LIBRARIES}")

# link the release version of the open3d library
target_link_libraries(${SHARED_LIB_NAME} PUBLIC Open3D::Open3D)

# On Windows if BUILD_SHARED_LIBS is enabled, copy .dll files to the executable directory
if(WIN32)
    get_target_property(open3d_type Open3D::Open3D TYPE)
    if(open3d_type STREQUAL "SHARED_LIBRARY")
        message(STATUS "Copying Open3D.dll to ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_BUILD_TYPE}")
        add_custom_command(TARGET ${SHARED_LIB_NAME} POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy
            $<TARGET_FILE:Open3D::Open3D>
            $<TARGET_FILE_DIR:${SHARED_LIB_NAME}>)
    endif()
endif()

# Boost (header only) -----------------------------------------------------
download_submodule_project(boost)
target_include_directories(${SHARED_LIB_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/deps/boost/win/1_89/include/boost-1_85)

# CGAL (header-only) ------------------------------------------------------
target_include_directories(${SHARED_LIB_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/deps/cgal/include)

# Cilantro (header-only) --------------------------------------------------
download_submodule_project(cilantro)
target_include_directories(${SHARED_LIB_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/deps/submodule-cilantro/include)

# loguru (header-only) ----------------------------------------------------
download_submodule_project(loguru)
add_subdirectory(deps/loguru)
target_link_libraries(${SHARED_LIB_NAME} PUBLIC loguru::loguru)

#--------------------------------------------------------------------------
# executable for prototyping
#--------------------------------------------------------------------------
set(APP_NAME_EXE diffCheckApp)

add_executable(${APP_NAME_EXE} src/diffCheckApp.cc)

set_target_properties(${APP_NAME_EXE} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    )

target_link_libraries(${APP_NAME_EXE} ${SHARED_LIB_NAME})

target_include_directories(${APP_NAME_EXE}
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src
    )

#--------------------------------------------------------------------------
# pybind11
#--------------------------------------------------------------------------
if (BUILD_PYTHON_MODULE)
    set(PYBINDMODULE_NAME diffcheck_bindings)
    set(PYPI_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src/gh/diffCheck/diffCheck)
    set(TARGET_DLL_PYPI_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src/gh/diffCheck/diffCheck/dlls)
    set(SPHINX_DOC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/doc)

    download_submodule_project(pybind11)
    add_subdirectory(deps/pybind11)

    find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

    message(STATUS "Python3_EXECUTABLE: ${Python3_EXECUTABLE}")
    message(STATUS "Python3_INCLUDE_DIRS: ${Python3_INCLUDE_DIRS}")
    message(STATUS "Python3_LIBRARIES: ${Python3_LIBRARIES}")
    message(STATUS "Python3_VERSION: ${Python3_VERSION}")

    set(PYBIND11_PYTHON_VERSION 3.9.10)

    pybind11_add_module(${PYBINDMODULE_NAME} src/diffCheckBindings.cc)

    target_link_libraries(${PYBINDMODULE_NAME} PUBLIC ${SHARED_LIB_NAME})
    target_include_directories(${PYBINDMODULE_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)

    # copy the pyd file to the pypi directory
    add_custom_command(TARGET ${PYBINDMODULE_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
        $<TARGET_FILE:${PYBINDMODULE_NAME}>
        ${PYPI_DIR}
        )
    copy_dlls(${TARGET_DLL_PYPI_DIR} ${PYBINDMODULE_NAME})
    # copy the pyd/dlls for the sphinx documentation
    add_custom_command(TARGET ${PYBINDMODULE_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
        $<TARGET_FILE:${PYBINDMODULE_NAME}>
        ${SPHINX_DOC_DIR}
        )
    copy_dlls(${SPHINX_DOC_DIR} ${PYBINDMODULE_NAME})
endif()

#--------------------------------------------------------------------------
# Tests
#--------------------------------------------------------------------------
if(BUILD_TESTS)
    include(tests)
endif()