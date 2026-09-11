# This script is executed at build time to copy DLLs
# It uses variables passed from the main CMake configuration

# Remove old DLLs from the destination directory
file(GLOB old_dlls "${DIR_TO_CLEAN}/*.dll")
if(old_dlls)
    file(REMOVE ${old_dlls})
endif()

# Get all DLLs from the source directory (evaluated at build time)
file(GLOB dll_files "${SRC_DIR}/*.dll")

# Copy each DLL to the destination directory
foreach(dll_file ${dll_files})
    get_filename_component(dll_name ${dll_file} NAME)
    message(STATUS "Copying ${dll_name} to ${DST_DIR}")
    file(COPY ${dll_file} DESTINATION ${DST_DIR})
endforeach()
