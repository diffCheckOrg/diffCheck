# The options need to be the same as Open3D's default
# If Open3D is configured and built with custom options, you'll also need to
# specify the same custom options.
option(STATIC_WINDOWS_RUNTIME "Use static (MT/MTd) Windows runtime" ON)

option(SILENT_LOGGING "Do not log messages in the terminal if on." OFF)

# To build the python bindings
option(BUILD_PYTHON_MODULE "Build the python bindings" ON)

# Build/Run tests
option(BUILD_TESTS "Build test suites" ON)
option(RUN_TESTS "Run test suites" ON)