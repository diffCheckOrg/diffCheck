#include "visualizer.hh"


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
        open3d::visualization::DrawGeometries(
            this->m_Geometries,
            this->Title,
            this->Width,
            this->Height,
            this->PosX, this->PosY,
            this->ShowNormals,
            this->ShowWireframe);
    }
} // namespace diffCheck::visualizer