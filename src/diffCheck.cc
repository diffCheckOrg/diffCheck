#pragma once

#include "diffCheck.hh"  // This is a dummy include to test the include path
#include <open3d/Open3D.h>

#include <string>
#include <iostream>

namespace diffCheck {

    int func1() { diffCheck::testHeaderCheck1(); return 1;}
    int func2() { diffCheck::testHeaderCheck2(); return 2;}
    int func3() { diffCheck::testHeaderCheck3(); return 3;}

    void testOpen3d()
    {
        std::shared_ptr<open3d::geometry::PointCloud> cloud(new open3d::geometry::PointCloud());
        std::cout << "testOpen3d check." << std::endl;
    }

}  // namespace diffCheck