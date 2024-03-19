#include "DFPointCloud.hh"

#include "diffCheck/IOManager.hh"


namespace diffCheck::geometry
{
    void DFPointCloud::Cvt2DFPointCloud(const std::shared_ptr<open3d::geometry::PointCloud> &O3DPointCloud)
    {
        if (O3DPointCloud->points_.size() != 0)
            for (auto &point : O3DPointCloud->points_)
                this->Points.push_back(point);
        if (O3DPointCloud->HasColors())
            for (auto &color : O3DPointCloud->colors_)
                this->Colors.push_back(color);
        if (O3DPointCloud->HasNormals())
            for (auto &normal : O3DPointCloud->normals_)
                this->Normals.push_back(normal);
    }

    std::shared_ptr<open3d::geometry::PointCloud> DFPointCloud::Cvt2O3DPointCloud()
    {
        std::shared_ptr<open3d::geometry::PointCloud> O3DPointCloud(new open3d::geometry::PointCloud());
        if (this->Points.size() != 0)
            for (auto &point : this->Points)
                O3DPointCloud->points_.push_back(point);
        if (this->Colors.size() != 0)
            for (auto &color : this->Colors)
                O3DPointCloud->colors_.push_back(color);
        if (this->Normals.size() != 0)
            for (auto &normal : this->Normals)
                O3DPointCloud->normals_.push_back(normal);
        return O3DPointCloud;
    }

    void DFPointCloud::LoadFromPLY(const std::string &path)
    {
        auto cloud = diffCheck::io::ReadPLYPointCloud(path);

        this->Points = cloud->Points;
        this->Colors = cloud->Colors;
        this->Normals = cloud->Normals;
    }
}