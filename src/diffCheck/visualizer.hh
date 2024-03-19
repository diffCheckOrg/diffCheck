#pragma once

#include <igl/opengl/glfw/Viewer.h>
#include <Eigen/Core>

#include "diffCheck/geometry/DFPointCloud.hh"

namespace diffCheck::visualizer
{
    class Visualizer
    {
    public:
        Visualizer()
        {
            m_Viewer = igl::opengl::glfw::Viewer();
        };
        ~Visualizer() = default;

        /**
         * @brief Load a point cloud to visualize
         * 
         * @param pointCloud the point cloud to visualize
         */
        void LoadPointCloud(std::shared_ptr<diffCheck::geometry::DFPointCloud> &pointCloud);

        // TODO: implement the  diffCHeck mesh object
        /**
         * @brief Load a mesh to visualize
         * 
         * @param mesh the mesh to visualize
         */
        void LoadMesh(const Eigen::MatrixXd &V, const Eigen::MatrixXi &F);

        /// @brief Main function to start the visualizer
        void Run();

    private:
        /// @brief The viewer object from libigl
        igl::opengl::glfw::Viewer m_Viewer;
        /// @brief The vertices of the mesh
        Eigen::MatrixXd m_V;
        /// @brief The faces of the mesh
        Eigen::MatrixXi m_F;
    };
}  // namespace diffCheck::visualizer