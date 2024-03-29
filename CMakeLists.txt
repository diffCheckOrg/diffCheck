cmake_minimum_required(VERSION 3.16.)
project(DiffCheck VERSION 1.0.0 LANGUAGES CXX C)
set(CMAKE_CXX_STANDARD 17)

list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

# import the custom cmake utilities funcs
include(external_tools)

# do a submodule init if not done already
execute_process(COMMAND git submodule update --init --recursive
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    RESULT_VARIABLE GIT_SUBMOD_RESULT
    )
if(NOT GIT_SUBMOD_RESULT EQUAL "0")
    message(FATAL_ERROR "git submodule update --init --recursive failed with ${GIT_SUBMOD_RESULT}, please checkout submodules")
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


#--------------------------------------------------------------------------
# 3rd party
#--------------------------------------------------------------------------

# Eigen -------------------------------------------------------------------
download_submodule_project(eigen)
add_subdirectory(deps/eigen)
target_link_libraries(${SHARED_LIB_NAME} PUBLIC Eigen3::Eigen)

# Open3D (pre-built binaries) -----------------------------------------------------    
# The options need to be the same as Open3D's default
# If Open3D is configured and built with custom options, you'll also need to
# specify the same custom options.
option(STATIC_WINDOWS_RUNTIME "Use static (MT/MTd) Windows runtime" ON)
if(STATIC_WINDOWS_RUNTIME)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
else()
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
endif()

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
        message(STATUS "Copying Open3D.dll to ${CMAKE_CURRENT_BINARY_DIR}/$<CONFIG>")
        add_custom_command(TARGET ${SHARED_LIB_NAME} POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different
            $<TARGET_FILE:Open3D::Open3D>
            $<TARGET_FILE_DIR:${SHARED_LIB_NAME}>)
    endif()
endif()

# Boost (header only) -----------------------------------------------------
download_submodule_project(boost)
target_link_directories(${SHARED_LIB_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/deps/boost/win/1_89/include/boost-1_85)

# print boost include dir
message(STATUS "Boost include dir: ${Boost_INCLUDE_DIRS}")

target_include_directories(${SHARED_LIB_NAME} PUBLIC ${Boost_INCLUDE_DIRS})

# CGAL (header-only) ------------------------------------------------------
target_include_directories(${SHARED_LIB_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/deps/cgal/include)

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
# Tests
#--------------------------------------------------------------------------

# include(CTest)
# enable_testing()

# add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/tests/global_registrations)