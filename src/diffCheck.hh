#pragma once

#include <igl/readPLY.h>
#include <igl/opengl/glfw/Viewer.h>

#include <open3d/Open3D.h>

// diffCheck includes
#include "diffCheck/libHeaderTemplate.hh"  // This is a dummy include to test the include path
#include "diffCheck/geometry/DFPointCloud.hh"
#include "diffCheck/IOManager.hh"
#include "diffCheck/visualizer.hh"


namespace diffCheck {
    /// @brief Function 1 of the library
    int func1();

    /// @brief Function 2 of the library
    int func2();

    /// @brief Function 3 of the library
    int func3();

    /// @brief Testing open3d import
    void testOpen3d();
}  // namespace diffCheck