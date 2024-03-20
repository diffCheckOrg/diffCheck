#pragma once

#include <igl/opengl/glfw/Viewer.h>
#include <Eigen/Core>

#include "diffCheck/geometry/DFPointCloud.hh"
#include "diffCheck/geometry/DFMesh.hh"

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

        // TODO: need to implement color and normals for meshes
        /**
         * @brief Load a mesh to visualize
         * 
         * @param std::shared_ptr<diffCheck::geometry::DFMesh> the mesh to visualize
         */
        void LoadMesh(std::shared_ptr<diffCheck::geometry::DFMesh> &mesh);

        /// @brief Main function to start the visualizer
        void Run();

    private:
        /// @brief The viewer object from libigl
        igl::opengl::glfw::Viewer m_Viewer;
        /// @brief The vertices of the mesh
    };
}  // namespace diffCheck::visualizer