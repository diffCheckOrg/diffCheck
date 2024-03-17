cmake_minimum_required(VERSION 3.16.)
project(DiffCheck VERSION 1.0.0 LANGUAGES CXX C)
set(CMAKE_CXX_STANDARD 17)


list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
include(external_tools)

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

target_precompile_headers(${SHARED_LIB_NAME} PUBLIC src/diffcheckpch.hh)

#--------------------------------------------------------------------------
# 3rd party
#--------------------------------------------------------------------------

# FIXME: problems with glfw (LINK : fatal error LNK1104: cannot open file '..\deps\glew\win\2_2_0\bin\Release\x64\glew32.obj' [F:\diffCheck\build\diffCheck.vcxproj])
# glfw --------------------------------------------------------------
add_subdirectory(deps/glfw)
target_link_libraries(${SHARED_LIB_NAME} PUBLIC glfw ${GLFW_LIBRARIES})
target_include_directories(${SHARED_LIB_NAME} PUBLIC ${GLFW_INCLUDE_DIRS})
target_link_libraries(${SHARED_LIB_NAME} INTERFACE glfw ${GLFW_LIBRARIES})
target_include_directories(${SHARED_LIB_NAME} INTERFACE ${GLFW_INCLUDE_DIRS})

# TODO: replace with add_subdirectory() instead of binaries
# glew --------------------------------------------------------------
set(GLEW_VERSION 2_2_0)  # 2.2.0
set(GLEW_LIB_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/glew/win/${GLEW_VERSION}/bin/Release/x64/glew32)
set(GLEW_INCLUDE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/glew/win/${GLEW_VERSION}/include)

target_link_libraries(${SHARED_LIB_NAME} PUBLIC ${GLEW_LIB_PATH})
target_link_libraries(${SHARED_LIB_NAME} INTERFACE ${GLEW_LIB_PATH})
target_include_directories(${SHARED_LIB_NAME} PUBLIC ${GLEW_INCLUDE_PATH})
target_include_directories(${SHARED_LIB_NAME} INTERFACE ${GLEW_INCLUDE_PATH})

# fmt --------------------------------------------------------------
add_subdirectory(deps/fmt)

target_link_libraries(${SHARED_LIB_NAME} PUBLIC fmt::fmt)
target_link_libraries(${SHARED_LIB_NAME} INTERFACE fmt::fmt)

# Eigen --------------------------------------------------------------
add_subdirectory(deps/eigen)

target_link_libraries(${SHARED_LIB_NAME} PUBLIC Eigen3::Eigen)
target_link_libraries(${SHARED_LIB_NAME} INTERFACE Eigen3::Eigen)

# Open3D --------------------------------------------------------------
set(O3D_VERSION 0_17)  # 0.17.0
set(OPEN3D_SHAREDLIB_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/open3d/win/${O3D_VERSION}/bin/Open3D)
set(OPEN3D_INCLUDE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/open3d/win/${O3D_VERSION}/include)

target_link_libraries(${SHARED_LIB_NAME} PUBLIC ${OPEN3D_SHAREDLIB_PATH})
target_link_libraries(${SHARED_LIB_NAME} INTERFACE ${OPEN3D_SHAREDLIB_PATH})
target_include_directories(${SHARED_LIB_NAME} PUBLIC ${OPEN3D_INCLUDE_PATH})
target_include_directories(${SHARED_LIB_NAME} INTERFACE ${OPEN3D_INCLUDE_PATH})


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