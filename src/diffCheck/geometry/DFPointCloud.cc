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

    std::vector<double> DFPointCloud::ComputeP2PDistance(std::shared_ptr<geometry::DFPointCloud> target)
    {
        std::vector<double> errors;
        auto O3DSourcePointCloud = this->Cvt2O3DPointCloud();
        auto O3DTargetPointCloud = target->Cvt2O3DPointCloud();
        
        std::vector<double> distances;

        distances = O3DSourcePointCloud->ComputePointCloudDistance(*O3DTargetPointCloud);
        return distances;
    }

    std::vector<Eigen::Vector3d> DFPointCloud::ComputeBoundingBox()
    {
        auto O3DPointCloud = this->Cvt2O3DPointCloud();
        auto boundingBox = O3DPointCloud->GetAxisAlignedBoundingBox();
        std::vector<Eigen::Vector3d> extremePoints;
        extremePoints.push_back(boundingBox.GetMinBound());
        extremePoints.push_back(boundingBox.GetMaxBound());
        return extremePoints;
    }

    std::vector<Eigen::Vector3d> DFPointCloud::GetTightBoundingBox()
    {
        open3d::geometry::OrientedBoundingBox tightOOBB = this->Cvt2O3DPointCloud()->GetMinimalOrientedBoundingBox();
        std::vector<Eigen::Vector3d> bboxPts = tightOOBB.GetBoxPoints();
        return bboxPts;
    }

    void DFPointCloud::ApplyTransformation(const diffCheck::transformation::DFTransformation &transformation)
    {
        auto O3DPointCloud = this->Cvt2O3DPointCloud();
        O3DPointCloud->Transform(transformation.TransformationMatrix);
        this->Points.clear();
        this->Colors.clear();
        this->Normals.clear();
        this->Cvt2DFPointCloud(O3DPointCloud);
    }

    void DFPointCloud::LoadFromPLY(const std::string &path)
    {
        auto cloud = diffCheck::io::ReadPLYPointCloud(path);

        this->Points = cloud->Points;
        this->Colors = cloud->Colors;
        this->Normals = cloud->Normals;
    }
}