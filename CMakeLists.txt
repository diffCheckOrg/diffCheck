cmake_minimum_required(VERSION 3.16.)
project(DiffCheck VERSION 1.0.0 LANGUAGES CXX C)
set(CMAKE_CXX_STANDARD 17)


list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)


#--------------------------------------------------------------------------
# refresh deps gitmodules
#--------------------------------------------------------------------------

include(external_tools)

#FIXME: here we need to use the external function to update the submodules to the
# latest commit
execute_process(COMMAND git submodule update --init --recursive
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    RESULT_VARIABLE GIT_SUBMOD_RESULT
    )
# do a git pull to get the latest commit
execute_process(COMMAND git pull
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    RESULT_VARIABLE GIT_PULL_RESULT
    )
if(NOT GIT_SUBMOD_RESULT EQUAL "0")
    message(FATAL_ERROR "git submodule update --init --recursive failed with ${GIT_SUBMOD_RESULT}, please checkout submodules")
endif()


#--------------------------------------------------------------------------
# library
#--------------------------------------------------------------------------

set(SHARED_LIB_NAME diffCheck)

file(GLOB_RECURSE SOURCES_LIB 
    src/diffCheck.cc src/diffCheck.hh        # diffCheck interface
    src/diffCheck/*.cc src/diffCheck/*.hh    # diffCheck src
    src/diffcheckpch.cc src/diffcheckpch.hh  # precompiled headers
    )

add_library(${SHARED_LIB_NAME} SHARED ${SOURCES_LIB})

if (WIN32)
    set_target_properties(${SHARED_LIB_NAME} PROPERTIES
        WINDOWS_EXPORT_ALL_SYMBOLS TRUE
        )
endif()
    set_target_properties(${SHARED_LIB_NAME} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin  # for dll
        # ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin  # for lib
        )

target_include_directories(${SHARED_LIB_NAME}
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src
    )

# target_precompile_headers(${SHARED_LIB_NAME} PUBLIC src/diffcheckpch.hh)

#--------------------------------------------------------------------------
# 3rd party
#--------------------------------------------------------------------------







# FIXME: problems with glfw (LINK : fatal error LNK1104: cannot open file '..\deps\glew\win\2_2_0\bin\Release\x64\glew32.obj' [F:\diffCheck\build\diffCheck.vcxproj])
# glfw (pre-build binaries) --------------------------------------------------------------

# TODO: add binaries to deps
set(GLFW_VERSION 3_3_4)  # 3.3.4
set(GLFW_LIB_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/glfw/win/${GLFW_VERSION}/lib-vc2019)
set(GLFW_INCLUDE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/glfw/win/${GLFW_VERSION}/include)

add_library(glfw3 SHARED IMPORTED)
set_target_properties(glfw3 PROPERTIES
    IMPORTED_LOCATION ${GLFW_LIB_PATH}/glfw3.dll
    IMPORTED_IMPLIB ${GLFW_LIB_PATH}/glfw3.lib
    INTERFACE_INCLUDE_DIRECTORIES ${GLFW_INCLUDE_PATH}
    )

target_link_libraries(${SHARED_LIB_NAME} PUBLIC glfw3)
target_include_directories(${SHARED_LIB_NAME} PUBLIC ${GLFW_INCLUDE_PATH})

# TODO: replace with add_subdirectory() instead of binaries
# glew (pre-build binaries) --------------------------------------------------------------
set(GLEW_VERSION 2_2_0)  # 2.2.0
set(GLEW_LIB_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/glew/win/${GLEW_VERSION}/bin/Release/x64)
set(GLEW_STATIC_LIB_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/glew/win/${GLEW_VERSION}/lib/Release/x64)
set(GLEW_INCLUDE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/glew/win/${GLEW_VERSION}/include)

add_library(glew32 SHARED IMPORTED)
set_target_properties(glew32 PROPERTIES
    IMPORTED_LOCATION ${GLEW_LIB_PATH}/glew32.dll
    IMPORTED_IMPLIB ${GLEW_STATIC_LIB_PATH}/glew32.lib
    INTERFACE_INCLUDE_DIRECTORIES ${GLEW_INCLUDE_PATH}
    )


# target_link_directories(${SHARED_LIB_NAME} PUBLIC ${GLEW_STATIC_LIB_PATH})
# target_link_directories(${SHARED_LIB_NAME} INTERFACE ${GLEW_STATIC_LIB_PATH})
# target_link_directories(${SHARED_LIB_NAME} PUBLIC ${GLEW_LIB_PATH})
# target_link_directories(${SHARED_LIB_NAME} INTERFACE ${GLEW_LIB_PATH})

target_link_libraries(${SHARED_LIB_NAME} PUBLIC glew32)
# target_link_libraries(${SHARED_LIB_NAME} INTERFACE glew32)
target_include_directories(${SHARED_LIB_NAME} PUBLIC ${GLEW_INCLUDE_PATH})
# target_include_directories(${SHARED_LIB_NAME} INTERFACE ${GLEW_INCLUDE_PATH})

# fmt (header-only)--------------------------------------------------------------
add_subdirectory(deps/fmt)

target_link_libraries(${SHARED_LIB_NAME} PUBLIC fmt::fmt)
# target_link_libraries(${SHARED_LIB_NAME} INTERFACE fmt::fmt)

# Eigen (header-only)--------------------------------------------------------------
add_subdirectory(deps/eigen)

target_link_libraries(${SHARED_LIB_NAME} PUBLIC Eigen3::Eigen)
# target_link_libraries(${SHARED_LIB_NAME} INTERFACE Eigen3::Eigen)



# FIXME: no need to specify opnegl because by system and fetched automatically
# # # OpenGL (from system) --------------------------------------------------------------
find_package(OpenGL REQUIRED)
target_link_libraries(${SHARED_LIB_NAME} PUBLIC OpenGL::GL)
target_link_libraries(${SHARED_LIB_NAME} INTERFACE OpenGL::GL)







# HERE'S THE PROBLEEEEEM <<<<<<
# Libigl (header-only) --------------------------------------------------------------

# all dependecies for libigl: https://libigl.github.io/third-party/
# set compiling flags for libigl
set(LIBIGL_USE_STATIC_LIBRARY OFF)
set(LIBIGL_GLFW ON)
add_subdirectory(deps/libigl)

target_link_libraries(${SHARED_LIB_NAME} PUBLIC igl::glfw)
# target_link_libraries(${SHARED_LIB_NAME} INTERFACE igl::core igl::opengl igl::opengl_glfw)

# set(LIBIGL_INCLUDE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/libigl/include)
# target_include_directories(${SHARED_LIB_NAME} PUBLIC ${LIBIGL_INCLUDE_PATH})
# target_include_directories(${SHARED_LIB_NAME} INTERFACE ${LIBIGL_INCLUDE_PATH})










# Open3D (pre-build binaries /headless not visuals)--------------------------------------------------------------
set(O3D_VERSION 0_17)  # 0.17.0
set(OPEN3D_SHAREDLIB_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/open3d/win/${O3D_VERSION}/bin)
set(OPEN3D_LIB_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/open3d/win/${O3D_VERSION}/lib)
set(OPEN3D_INCLUDE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/open3d/win/${O3D_VERSION}/include)

add_library(Open3D SHARED IMPORTED)
set_target_properties(Open3D PROPERTIES
    IMPORTED_LOCATION ${OPEN3D_SHAREDLIB_PATH}/Open3D.dll
    IMPORTED_IMPLIB ${OPEN3D_LIB_PATH}/Open3D.lib
    INTERFACE_INCLUDE_DIRECTORIES ${OPEN3D_INCLUDE_PATH}
    )

target_link_libraries(${SHARED_LIB_NAME} PUBLIC Open3D)
# target_link_libraries(${SHARED_LIB_NAME} INTERFACE Open3D)
target_include_directories(${SHARED_LIB_NAME} PUBLIC ${OPEN3D_INCLUDE_PATH})
# target_include_directories(${SHARED_LIB_NAME} INTERFACE ${OPEN3D_INCLUDE_PATH})




# copy all the dlls to the bin directory to make dll accessible
# List of dynamic libraries that DiffCheck is linked against
set(DEPENDENCIES glfw3 glew32 Open3D)

foreach(DEP_LIB ${DEPENDENCIES})
    add_custom_command(TARGET ${SHARED_LIB_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        $<TARGET_FILE:${DEP_LIB}>
        $<TARGET_FILE_DIR:${SHARED_LIB_NAME}>
    )
endforeach()


#--------------------------------------------------------------------------
# executable
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