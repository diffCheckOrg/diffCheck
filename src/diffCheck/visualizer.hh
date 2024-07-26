#pragma once

#include <memory>
#include <vector>

#include <open3d/Open3D.h>

#include <Eigen/Core>

#include "diffCheck/geometry/DFPointCloud.hh"
#include "diffCheck/geometry/DFMesh.hh"

namespace diffCheck::visualizer
{
    class Visualizer
    {
    public:
        Visualizer(
            std::string title = "DiffCheckApp",
            int width = 1000,
            int height = 800,
            int posX = 50,
            int posY = 50,
            bool showNormals = true,
            bool showWireframe = true,
            bool renderPcdColorNormals = false
            ) : Title(title), Width(width), Height(height),
                PosX(posX), PosY(posY),
                ShowNormals(showNormals), ShowWireframe(showWireframe),
                RenderPcdColorNormals(renderPcdColorNormals)
        {}
        ~Visualizer() = default;

    public:
        /**
         * @brief Load a point cloud to visualize
         * 
         * @param pointCloud the point cloud to visualize
         */
        void AddPointCloud(std::shared_ptr<diffCheck::geometry::DFPointCloud> &pointCloud);

        /**
         * @brief Load a mesh to visualize
         * 
         * @param std::shared_ptr<diffCheck::geometry::DFMesh> the mesh to visualize
         */
        void AddMesh(std::shared_ptr<diffCheck::geometry::DFMesh> &mesh);

        /// @brief Main function to start the visualizer
        void Run();

    public:
        /// @brief title of the window
        std::string Title;
        /// @brief width of the window
        int Width;
        /// @brief height of the window
        int Height;
        /// @brief position of the window
        int PosX;
        /// @brief position of the window
        int PosY;
        /// @brief weither to show the normals
        bool ShowNormals;
        /// @brief weither to show the wireframe
        bool ShowWireframe;
        /// @brief weither to render the point cloud color normals
        bool RenderPcdColorNormals;

    private:
        /// @brief the geometries to visualize
        std::vector<std::shared_ptr<const open3d::geometry::Geometry>, std::allocator<std::shared_ptr<const open3d::geometry::Geometry>>> m_Geometries;
    };
}  // namespace diffCheck::visualizer