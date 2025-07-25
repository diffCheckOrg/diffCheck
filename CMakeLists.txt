cmake_minimum_required(VERSION 3.16.)
project(diffCheck VERSION 1.3.0 LANGUAGES CXX C)
set(CMAKE_CXX_STANDARD 17)

# Force usage of libc++ and proper visibility on macOS
# For some reason, without this, there will be a segfault in test
if(APPLE)
    add_compile_options(-stdlib=libc++ -fvisibility=hidden -Wall)
    add_link_options(-stdlib=libc++)
endif()

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
    src/diffCheck.hh                          # diffCheck interface
    src/diffCheck/*.cc src/diffCheck/*.hh     # diffCheck src
)

# For some reason, on macOS, we need to compile the library as static
# I wonder if it's a good idea to also compile the library as static on Windows
# if (APPLE)
    # add_library(${SHARED_LIB_NAME} STATIC ${SOURCES_LIB})
# else()
add_library(${SHARED_LIB_NAME} STATIC ${SOURCES_LIB})
# endif()

if (WIN32)
    set_target_properties(${SHARED_LIB_NAME} PROPERTIES
        WINDOWS_EXPORT_ALL_SYMBOLS TRUE
        )
endif()

set_target_properties(${SHARED_LIB_NAME} PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
)

target_include_directories(${SHARED_LIB_NAME}
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# set the MD_DynamicRelease flag for MSVC since we are compiling with /MD for py wrap
if (WIN32)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
endif()

#--------------------------------------------------------------------------
# 3rd party
#--------------------------------------------------------------------------

# Eigen -------------------------------------------------------------------
download_submodule_project(eigen)
add_subdirectory(deps/eigen)
target_link_libraries(${SHARED_LIB_NAME} PUBLIC Eigen3::Eigen)

# Open3D (pre-built binaries) ---------------------------------------------
# download_submodule_project(open3d)
if (WIN32)
    set(Open3D_DIR ${CMAKE_CURRENT_SOURCE_DIR}/deps/open3d/win/0_18/CMake)    
elseif (APPLE)
    set(Open3D_DIR ${CMAKE_CURRENT_SOURCE_DIR}/deps/open3d/mac/open3d-devel-darwin-arm64-0.18.0/lib/cmake/Open3D)
endif()
find_package(Open3D 0.18.0 REQUIRED)

# find_package(Open3D HINTS ${CMAKE_INSTALL_PREFIX}/lib/cmake)

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
add_definitions(-D_GLIBCXX_DEBUG)

if (BUILD_PYTHON_MODULE)
    set(PYBINDMODULE_NAME diffcheck_bindings)
    set(PYPI_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src/gh/diffCheck/diffCheck)
    set(TARGET_DLL_PYPI_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src/gh/diffCheck/diffCheck/dlls)
    set(TARGET_SO_PYPI_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src/gh/diffCheck/diffCheck)
    set(SPHINX_DOC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/doc)

    download_submodule_project(pybind11)
    add_subdirectory(deps/pybind11)

    find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

    message(STATUS "Python3_EXECUTABLE: ${Python3_EXECUTABLE}")
    message(STATUS "Python3_INCLUDE_DIRS: ${Python3_INCLUDE_DIRS}")
    message(STATUS "Python3_LIBRARIES: ${Python3_LIBRARIES}")
    message(STATUS "Python3_VERSION: ${Python3_VERSION}")

    set(PYBIND11_PYTHON_VERSION 3.9.10)

    pybind11_add_module(${PYBINDMODULE_NAME}
        MODULE
        src/diffCheckBindings.cc
    )

    target_include_directories(${PYBINDMODULE_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)
    target_link_libraries(${PYBINDMODULE_NAME} PUBLIC ${SHARED_LIB_NAME})

    # copy the pyd file to the pypi directory
    add_custom_command(TARGET ${PYBINDMODULE_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
        $<TARGET_FILE:${PYBINDMODULE_NAME}>
        ${PYPI_DIR}
        )
    # copy the pyd/dlls for the sphinx documentation
    add_custom_command(TARGET ${PYBINDMODULE_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
        $<TARGET_FILE:${PYBINDMODULE_NAME}>
        ${SPHINX_DOC_DIR}
        )

    if (WIN32)
        copy_dlls(${TARGET_DLL_PYPI_DIR} ${PYBINDMODULE_NAME})
        copy_dlls(${SPHINX_DOC_DIR} ${PYBINDMODULE_NAME})
    elseif (APPLE)
        copy_so_files(${TARGET_SO_PYPI_DIR} ${PYBINDMODULE_NAME})
        copy_so_files(${SPHINX_DOC_DIR} ${PYBINDMODULE_NAME})
    endif()
endif()

# install the diffCheck shared library to the system path
install(TARGETS ${SHARED_LIB_NAME}
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

#--------------------------------------------------------------------------
# Tests
#--------------------------------------------------------------------------
if(BUILD_TESTS)
    include(tests)
endif()