cmake_minimum_required(VERSION 3.16.)
project(DiffCheck VERSION 1.0.0 LANGUAGES CXX C)
set(CMAKE_CXX_STANDARD 17)

# set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")

# # enable MT option for diffcheck
# set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
# set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Release>:Release>DLL")


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
    # src/diffCheck/*.cc src/diffCheck/*.hh    # diffCheck src  # TODO: temp reactivate
    src/IOManager.cc src/IOManager.hh         # IOManager TOOD: a test erase
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
# # fmt ---------------------------------------------------------------------
# download_submodule_project(fmt)
# add_subdirectory(deps/fmt)
# target_link_libraries(${SHARED_LIB_NAME} PUBLIC fmt::fmt)

# Eigen -------------------------------------------------------------------
download_submodule_project(eigen)
add_subdirectory(deps/eigen)
target_link_libraries(${SHARED_LIB_NAME} PUBLIC Eigen3::Eigen)

# # OpenGL (from system) ----------------------------------------------------
# find_package(OpenGL REQUIRED)
# target_link_libraries(${SHARED_LIB_NAME} PUBLIC OpenGL::GL)
# target_link_libraries(${SHARED_LIB_NAME} INTERFACE OpenGL::GL)

# # Libigl + glfw -----------------------------------------------------------
download_submodule_project(libigl)
# all dependecies for libigl: https://libigl.github.io/third-party/
# set compiling flags for libigl
set(LIBIGL_USE_STATIC_LIBRARY OFF)
set(LIBIGL_GLFW ON)
add_subdirectory(deps/libigl)

target_link_libraries(${SHARED_LIB_NAME} PUBLIC igl::glfw)


# # glew (binaries) ------------------------------------------------------
# # download_submodule_project(glew)
# set(GLEW_LIB_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/glew/lib/Release/x64)
# set(GLEW_INCLUDE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/glew/include)

# add_library(GLEW SHARED IMPORTED)
# set_target_properties(GLEW PROPERTIES
#     IMPORTED_LOCATION ${GLEW_LIB_PATH}/glew32.dll
#     IMPORTED_IMPLIB ${GLEW_LIB_PATH}/glew32.lib
#     INTERFACE_INCLUDE_DIRECTORIES ${GLEW_INCLUDE_PATH}
#     )

# target_link_libraries(${SHARED_LIB_NAME} PUBLIC GLEW)
# target_include_directories(${SHARED_LIB_NAME} PUBLIC ${GLEW_INCLUDE_PATH})

# # glfw (compile from source) ------------------------------------------------------
# download_submodule_project(glfw)
# add_subdirectory(deps/glfw)

# target_link_libraries(${SHARED_LIB_NAME} PUBLIC glfw)





# # Open3D (pre-build binaries /headless not visuals)------------------------

# # The options need to be the same as Open3D's default
# # If Open3D is configured and built with custom options, you'll also need to
# # specify the same custom options.
# option(STATIC_WINDOWS_RUNTIME "Use static (MT/MTd) Windows runtime" ON)
# if(STATIC_WINDOWS_RUNTIME)
#     set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
# else()
#     set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
# endif()

# download_submodule_project(open3d)  # TODO: temp reactivate
# set(O3D_VERSION 0_18)  # 0.18.0
# set(OPEN3D_SHAREDLIB_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/open3d/win/${O3D_VERSION}/bin)
# set(OPEN3D_LIB_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/open3d/win/${O3D_VERSION}/lib)
# set(OPEN3D_INCLUDE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/open3d/win/${O3D_VERSION}/include)

# # import open3d as a static lib
# add_library(Open3D STATIC IMPORTED)
# set_target_properties(Open3D PROPERTIES
#     IMPORTED_LOCATION ${OPEN3D_LIB_PATH}/Open3D.lib
#     INTERFACE_INCLUDE_DIRECTORIES ${OPEN3D_INCLUDE_PATH}
#     )

# target_link_libraries(${SHARED_LIB_NAME} PUBLIC Open3D)
# target_include_directories(${SHARED_LIB_NAME} PUBLIC ${OPEN3D_INCLUDE_PATH})

# # copy the o3d dll to the binary dir to make it available for the app
# set(DEPENDENCIES Open3D)

# foreach(DEP_LIB ${DEPENDENCIES})
#     add_custom_command(TARGET ${SHARED_LIB_NAME} POST_BUILD
#         COMMAND ${CMAKE_COMMAND} -E copy_if_different
#         $<TARGET_FILE:${DEP_LIB}>
#         $<TARGET_FILE_DIR:${SHARED_LIB_NAME}>
#     )
# endforeach()

# # CGAL ( ctories(${SHARED_LIB_NAME} PUBLIC ${CGAL_INCLUDE_DIRS})



# Open3D (from system) -----------------------------------------------------    
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

# Boost (header-only) -----------------------------------------------------
# download_submodule_project(boost)
# add_subdirectory(deps/boost)
# target_include_directories(${SHARED_LIB_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/deps/boost/include)

# CGAL (header-only) ------------------------------------------------------
# download_submodule_project(cgal)
# add_subdirectory(deps/cgal)
# target_include_directories(${SHARED_LIB_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/deps/cgal/include)


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