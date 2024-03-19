#include "diffCheck.hh"

// #include <open3d/Open3D.h>

#include <string>
#include <iostream>

namespace diffCheck {

    int func1() { diffCheck::testHeaderCheck1(); return 1;}
    int func2() { diffCheck::testHeaderCheck2(); return 2;}
    int func3() { diffCheck::testHeaderCheck3(); return 3;}

    void testOpen3d()
    {
        // std::shared_ptr<open3d::geometry::PointCloud> cloud(new open3d::geometry::PointCloud());
        // // print the number of points in the point cloud
        // std::cout << "Point cloud has " << cloud->points_.size() << " points." << std::endl;
        // std::cout << "testOpen3d check." << std::endl;

        // // fill the point cloud with random points
        // cloud->points_.resize(100);
        // for (auto &point : cloud->points_) {
        //     point = Eigen::Vector3d::Random();
        // }
        // // set the point cloud color to be light blue
        // cloud->colors_.resize(100);
        // for (auto &color : cloud->colors_) {
        //     color = Eigen::Vector3d(0.7, 0.7, 1.0);
        // }
        // // set the normal of the point cloud
        // cloud->normals_.resize(100);
        // for (auto &normal : cloud->normals_) {
        //     normal = Eigen::Vector3d(0.0, 0.0, 1.0);
        // }
    }

    void testLibigl()
    {
        // // test pcd --------------
        // // Now you can use libigl
        // igl::opengl::glfw::Viewer viewer;

        // Eigen::MatrixXd V;
        // Eigen::MatrixXi F;
        // // Load a mesh in OFF format
        // igl::readPLY("bunny.ply", V, F);

        // // Plot the mesh
        // viewer.data().set_mesh(V, F);
        // viewer.launch();

        // ########################################
        const Eigen::MatrixXd V= (Eigen::MatrixXd(8,3)<<
            0.0,0.0,0.0,
            0.0,0.0,1.0,
            0.0,1.0,0.0,
            0.0,1.0,1.0,
            1.0,0.0,0.0,
            1.0,0.0,1.0,
            1.0,1.0,0.0,
            1.0,1.0,1.0).finished();
        const Eigen::MatrixXi F = (Eigen::MatrixXi(12,3)<<
            0,6,4,
            0,2,6,
            0,3,2,
            0,1,3,
            2,7,6,
            2,3,7,
            4,6,7,
            4,7,5,
            0,4,5,
            0,5,1,
            1,5,7,
            1,7,3).finished();

        // Plot the mesh
        igl::opengl::glfw::Viewer viewer;
        viewer.data().set_mesh(V, F);
        viewer.data().set_face_based(true);
        viewer.launch();
    }

}  // namespace diffCheck