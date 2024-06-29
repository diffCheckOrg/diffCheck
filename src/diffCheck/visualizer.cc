#include "visualizer.hh"

#include <open3d/visualization/visualizer/RenderOption.h>

namespace diffCheck::visualizer
{
    void Visualizer::AddPointCloud(std::shared_ptr<diffCheck::geometry::DFPointCloud> &pointCloud)
    {
        auto geometry = std::static_pointer_cast<const open3d::geometry::Geometry>(pointCloud->Cvt2O3DPointCloud());
        this->m_Geometries.push_back(geometry);
    }

    void Visualizer::AddMesh(std::shared_ptr<diffCheck::geometry::DFMesh> &mesh)
    {
        auto geometry = std::static_pointer_cast<const open3d::geometry::Geometry>(mesh->Cvt2O3DTriangleMesh());
        this->m_Geometries.push_back(geometry);
    }

    void Visualizer::Run()
    {
        auto vis = open3d::visualization::Visualizer();
        vis.CreateVisualizerWindow(this->Title, this->Width, this->Height, this->PosX, this->PosY);
        for (auto geometry : this->m_Geometries)
        {
            vis.AddGeometry(geometry);
        }
        vis.GetRenderOption().point_color_option_ = open3d::visualization::RenderOption::PointColorOption::Color;
        if (this->ShowNormals)
            vis.GetRenderOption().TogglePointShowNormal();
        vis.Run();
        vis.DestroyVisualizerWindow();
    }
} // namespace diffCheck::visualizer