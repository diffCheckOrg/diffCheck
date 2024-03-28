function(download_external_project project_name)
  include(CMakeParseArguments)

  set(_dep_flags
    NO_UPDATE)
  set(_dep_one_variables
    URL
    TAG
    BACKEND
    THIRD_PARTY_DIR
    PATCH
    )

  set(_dep_multi_variables)

  cmake_parse_arguments(_dep_args
    "${_dep_flags}"
    "${_dep_one_variables}"
    "${_dep_multi_variables}"
    ${ARGN}
    )

  if(NOT _dep_args_URL)
    message(FATAL_ERROR "You have to provide a URL for the project ${project_name}")
  endif()

  if(_dep_args_BACKEND)
    set(_ep_backend "${_dep_args_BACKEND}_REPOSITORY \"${_dep_args_URL}\"")
  else()
    set(_ep_backend "URL \"${_dep_args_URL}\"")
    if(CMAKE_VERSION VERSION_GREATER 3.23)
      list(APPEND _ep_backend "DOWNLOAD_EXTRACT_TIMESTAMP TRUE")
    endif()
  endif()

  if(_dep_args_TAG)
    set(_ep_tag "${_dep_args_BACKEND}_TAG ${_dep_args_TAG}")
  endif()


  if (NOT _dep_args_THIRD_PARTY_DIR)
    set(_dep_args_THIRD_PARTY_DIR deps)
  endif()

  if (_dep_args_PATCH)
    find_program(PATCH_EXECUTABLE patch REQUIRED)
    set(_patch_cmd "PATCH_COMMAND ${PATCH_EXECUTABLE} -p1 < \"${PROJECT_SOURCE_DIR}/${_dep_args_THIRD_PARTY_DIR}/${_dep_args_PATCH}\"")
  endif()

  set(_src_dir ${PROJECT_SOURCE_DIR}/${_dep_args_THIRD_PARTY_DIR}/${project_name})
  if(EXISTS ${_src_dir}/.DOWNLOAD_SUCCESS AND _dep_args_NO_UPDATE)
    return()
  endif()

  set(_working_dir ${PROJECT_BINARY_DIR}/${_dep_args_THIRD_PARTY_DIR}/${project_name}-download)
  set(_cmake_lists ${_working_dir}/CMakeLists.txt)
  file(WRITE  ${_cmake_lists} "cmake_minimum_required(VERSION 3.1)\n")
  file(APPEND ${_cmake_lists} "project(${project_name}-download NONE)\n")
  file(APPEND ${_cmake_lists} "include(ExternalProject)\n")
  file(APPEND ${_cmake_lists} "ExternalProject_Add(${project_name}\n")
  file(APPEND ${_cmake_lists} "    SOURCE_DIR ${_src_dir}\n")
  file(APPEND ${_cmake_lists} "    BINARY_DIR ${_working_dir}\n")
  foreach(line ${_ep_backend})
    file(APPEND ${_cmake_lists} "    ${line}\n")
  endforeach()
  file(APPEND ${_cmake_lists} "    ${_ep_tag}\n")
  file(APPEND ${_cmake_lists} "    CONFIGURE_COMMAND \"\"\n")
  file(APPEND ${_cmake_lists} "    BUILD_COMMAND     \"\"\n")
  file(APPEND ${_cmake_lists} "    INSTALL_COMMAND   \"\"\n")
  file(APPEND ${_cmake_lists} "    TEST_COMMAND      \"\"\n")
  file(APPEND ${_cmake_lists} "    ${_patch_cmd}\n")
  file(APPEND ${_cmake_lists} "LOG_BUILD 1)")

  message(STATUS "Downloading ${project_name} ${_dep_args_GIT_TAG}")
  execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" .
    RESULT_VARIABLE _result
    WORKING_DIRECTORY ${_working_dir}
    OUTPUT_FILE ${_working_dir}/download-out.log
    ERROR_FILE ${_working_dir}/download-error.log)

  if(_result)
    message(SEND_ERROR "Something went wrong (${_result}) during the download"
      " process of ${project_name} check the file"
      " ${_working_dir}/download-error.log for more details:")
    file(STRINGS "${_working_dir}/download-error.log" _error_strings)
    string(REPLACE ";" "\n" _error_msg "${_error_strings}")
    message(FATAL_ERROR "${_error_msg}")
  endif()

  execute_process(COMMAND "${CMAKE_COMMAND}" --build .
    RESULT_VARIABLE _result
    WORKING_DIRECTORY ${_working_dir}
    OUTPUT_FILE ${_working_dir}/build-out.log
    ERROR_FILE ${_working_dir}/build-error.log)

  if(_result)
    message("Something went wrong (${_result}) during the download"
      " process of ${project_name} check the file"
      " ${_working_dir}/build-error.log for more details")
    file(STRINGS "${_working_dir}/build-error.log" _error_strings)
    string(REPLACE ";" "\n" _error_msg "${_error_strings}")
    message(FATAL_ERROR "${_error_msg}")
  endif()

  file(WRITE ${_src_dir}/.DOWNLOAD_SUCCESS "")
endfunction()

# ------------------------------------------------------------------------------
function(mark_as_advanced_prefix prefix)
  get_property(_list DIRECTORY PROPERTY VARIABLES)
  foreach(_var ${_list})
    if("${_var}" MATCHES "^${prefix}")
      mark_as_advanced(${_var})
    endif()
  endforeach()
endfunction()

# ------------------------------------------------------------------------------
function(add_external_package package)
  include(CMakeParseArguments)

  set(_aep_flags
    IGNORE_SYSTEM
    )
  set(_aep_one_variables
    VERSION
    THIRD_PARTY_DIR
    )
  set(_aep_multi_variables)

  cmake_parse_arguments(_aep_args
    "${_aep_flags}"
    "${_aep_one_variables}"
    "${_aep_multi_variables}"
    ${ARGN}
    )

  if(_aep_args_VERSION)
    set(_${package}_version ${_aep_args_VERSION})
  endif()

  if (NOT _aep_args_THIRD_PARTY_DIR)
    set(_aep_args_THIRD_PARTY_DIR deps)
  endif()

  set(_cmake_includes ${PROJECT_SOURCE_DIR}/${_aep_args_THIRD_PARTY_DIR})
  set(_${package}_external_dir ${PROJECT_BINARY_DIR}/${_aep_args_THIRD_PARTY_DIR})


  if(NOT EXISTS ${_cmake_includes}/${package}.cmake)
    set(_required REQUIRED)
  endif()

  string(TOUPPER "${package}" u_package)
  if(NOT DEFINED  ${PROJECT_NAME}_USE_EXTERNAL_${u_package})
    set(${PROJECT_NAME}_USE_EXTERNAL_${u_package} FALSE CACHE INTERNAL "")
  endif()

  if(NOT _aep_args_IGNORE_SYSTEM AND NOT ${PROJECT_NAME}_USE_EXTERNAL_${u_package})
    find_package(${package} ${_${package}_version} ${_required} ${_aep_UNPARSED_ARGUMENTS} QUIET)
    if(${package}_FOUND AND NOT ${package}_FOUND_EXTERNAL)
      message(STATUS "Found system ${package}")
      string(TOUPPER ${package} u_package)
      mark_as_advanced_prefix(${package})
      mark_as_advanced_prefix(${u_package})
      return()
    endif()
  endif()

  if(EXISTS ${_cmake_includes}/${package}.cmake)
    message(STATUS "Using own ${package}")
    include(${_cmake_includes}/${package}.cmake)
    set(${PROJECT_NAME}_USE_EXTERNAL_${u_package} TRUE CACHE INTERNAL "")
  endif()
  string(TOUPPER ${package} u_package)
  mark_as_advanced_prefix(${package})
  mark_as_advanced_prefix(${u_package})
endfunction()

function(quote_arguments var)
  set(_quoted "")
  foreach(_arg ${ARGN})
    if(_quoted)
      set(_quoted "${_quoted}, \"${_arg}\"")
    else()
      set(_quoted "\"${_arg}\"")
    endif()
  endforeach()

  if(${var})
    set(${var} "${${var}}, ${_quoted}" PARENT_SCOPE)
  else()
    set(${var} "${_quoted}" PARENT_SCOPE)
  endif()
endfunction()

# Download and update submodules with latest remote version
function(download_submodule_project project_name)
  find_package(Git QUIET)
  if(NOT GIT_FOUND OR NOT EXISTS "${PROJECT_SOURCE_DIR}/.git" OR NOT EXISTS "${PROJECT_SOURCE_DIR}/deps/${project_name}/.git")
    return()
  endif()
  message(STATUS "Update submodule ${project_name} to the latest commit")

  execute_process(
    COMMAND ${GIT_EXECUTABLE} --version
    OUTPUT_VARIABLE GIT_VERSION_STRING
  )
  string(REGEX MATCH "([0-9]+)\\.([0-9]+)\\.([0-9]+)" GIT_VERSION_STRING ${GIT_VERSION_STRING})
  set(GIT_VERSION_MAJOR ${CMAKE_MATCH_1})
  set(GIT_VERSION_MINOR ${CMAKE_MATCH_2})
  set(GIT_VERSION_PATCH ${CMAKE_MATCH_3})

  if(NOT (GIT_VERSION_MAJOR GREATER 1 OR (GIT_VERSION_MAJOR EQUAL 1 AND GIT_VERSION_MINOR GREATER 8)))
    message(FATAL_ERROR "Git version 1.8 or greater is required.")
  endif()

  if(NOT EXISTS ${PROJECT_SOURCE_DIR}/deps/${project_name}/.git)
    execute_process(COMMAND ${GIT_EXECUTABLE} submodule init -- deps/${project_name}
      WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})
  endif()

  execute_process(COMMAND ${GIT_EXECUTABLE} submodule sync -- deps/${project_name}
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})
  execute_process(COMMAND ${GIT_EXECUTABLE} submodule update --init --recursive --remote -- deps/${project_name}
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
    RESULT_VARIABLE GIT_SUBMOD_RESULT)
  if(NOT GIT_SUBMOD_RESULT EQUAL "0")
    message(FATAL_ERROR "git submodule update --init --recursive --remote failed with ${GIT_SUBMOD_RESULT}, please checkout submodules")
  endif()
endfunction()