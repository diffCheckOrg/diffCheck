#include "DFPointCloud.hh"
#include "diffCheck/log.hh"

#include "diffCheck/IOManager.hh"


namespace diffCheck::geometry
{
    void DFPointCloud::Cvt2DFPointCloud(const std::shared_ptr<open3d::geometry::PointCloud> &O3DPointCloud)
    {
        this->Points.clear();
        this->Colors.clear();
        this->Normals.clear();

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

    void DFPointCloud::Cvt2DFPointCloud(const std::shared_ptr<cilantro::PointCloud3f> &cilantroPointCloud)
    {
        this->Points.clear();
        this->Colors.clear();
        this->Normals.clear();
        
        auto ptt = cilantroPointCloud->points;
        int n_pt = (int)ptt.cols();
        auto col = cilantroPointCloud->colors;
        auto nor = cilantroPointCloud->normals;

        if (n_pt == 0)
            throw std::invalid_argument("The point cloud is empty.");
        for (int i = 0; i < n_pt; i++)
        {
            Eigen::Vector3d pt_d = ptt.col(i).cast<double>();
            this->Points.push_back(pt_d);
        }

        if (cilantroPointCloud->hasColors())
        {
            for (int i = 0; i < n_pt; i++)
            {
                Eigen::Vector3d cl_d = col.col(i).cast <double>();
                this->Colors.push_back(cl_d);
            }
        }

        if (cilantroPointCloud->hasNormals())
        {
            for (int i = 0; i < n_pt; i++)
            {
                Eigen::Vector3d no_d = nor.col(i).cast <double>();
                this->Normals.push_back(no_d);
            }
        }
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

    std::shared_ptr<cilantro::PointCloud3f> DFPointCloud::Cvt2CilantroPointCloud()
    {
        std::shared_ptr<cilantro::PointCloud3f> cilantroPointCloud = std::make_shared<cilantro::PointCloud3f>();

        cilantro::VectorSet3f points;
        for (auto& pt : this->Points)
        {
            Eigen::Vector3f pt_f = pt.cast <float>();
            points.conservativeResize(points.rows(), points.cols() + 1);
            points.col(points.cols() - 1) = pt_f;
        }
        cilantroPointCloud->points = points;

        cilantro::VectorSet3f colors;
        if (this->HasColors())
        {
            for (auto& color : this->Colors)
            {
                Eigen::Vector3f color_f = color.cast <float>();
                colors.conservativeResize(colors.rows(), colors.cols() + 1);
                colors.col(colors.cols() - 1) = color_f;
            }
        }
        cilantroPointCloud->colors = colors;

        cilantro::VectorSet3f normals;
        if (this->HasNormals())
        {
            for (auto& normal : this->Normals)
            {
                Eigen::Vector3f normal_f = normal.cast <float>();
                normals.conservativeResize(normals.rows(), normals.cols() + 1);
                normals.col(normals.cols() - 1) = normal_f;
            }
        }
        cilantroPointCloud->normals = normals;

        return cilantroPointCloud;
    }

    std::vector<Eigen::Vector3d> DFPointCloud::GetAxixAlignedBoundingBox()
    {
        if (this->Points.empty()) {
            return {Eigen::Vector3d::Zero(), Eigen::Vector3d::Zero()};
        }

        Eigen::Vector3d minBound, maxBound;

#ifdef __APPLE__
        // Compute min and max bounds directly from points
        minBound = this->Points.front();
        maxBound = this->Points.front();

        for (const auto& point : this->Points) {
            minBound = minBound.cwiseMin(point);
            maxBound = maxBound.cwiseMax(point);
        }
#else
        auto O3DPointCloud = this->Cvt2O3DPointCloud();
        auto boundingBox = O3DPointCloud->GetAxisAlignedBoundingBox();

        boundingBox.GetMinBound());
        extremePoints.push_back(boundingBox.GetMaxBound());

#endif
        std::vector<Eigen::Vector3d> extremePoints;
        extremePoints.push_back(minBound);
        extremePoints.push_back(maxBound);

        return extremePoints;
    }

    void DFPointCloud::EstimateNormals(
        bool useCilantroEvaluator,
        std::optional<int> knn,
        std::optional<double> searchRadius
    )
    {
        if (!useCilantroEvaluator)
        {
            this->Normals.clear();
            auto O3DPointCloud = this->Cvt2O3DPointCloud();

            if (knn.value() != 30 && searchRadius.has_value() == false)
            {
                open3d::geometry::KDTreeSearchParamKNN knnSearchParam(knn.value());
                O3DPointCloud->EstimateNormals(knnSearchParam);
                DIFFCHECK_INFO(("Estimating normals with knn = " + std::to_string(knn.value())).c_str());
            }
            else if (searchRadius.has_value())
            {
                open3d::geometry::KDTreeSearchParamHybrid hybridSearchParam(searchRadius.value(), knn.value());
                O3DPointCloud->EstimateNormals(hybridSearchParam);
                DIFFCHECK_INFO(("Estimating normals with hybrid search radius = " + std::to_string(searchRadius.value()) + "and knn = " + std::to_string(knn.value())).c_str());
            }
            else
            {
                O3DPointCloud->EstimateNormals();
                DIFFCHECK_INFO("Default estimation of normals with knn = 30");
            }
            for (auto &normal : O3DPointCloud->normals_)
                this->Normals.push_back(normal);
        }
        else
        {
            std::shared_ptr<cilantro::PointCloud3f> cilantroPointCloud = this->Cvt2CilantroPointCloud();
            cilantro::KNNNeighborhoodSpecification<int> neighborhood(knn.value());
            cilantroPointCloud->estimateNormals(neighborhood, false);

            this->Normals.clear();
            for (int i = 0; i < cilantroPointCloud->normals.cols(); i++)
                this->Normals.push_back(cilantroPointCloud->normals.col(i).cast<double>());
            DIFFCHECK_INFO(("Estimating normals with cilantro evaluator with knn = " + std::to_string(knn.value())).c_str());
        }

    }

    void DFPointCloud::VoxelDownsample(double voxelSize)
    {
        if (voxelSize <= 0)
            throw std::invalid_argument("Voxel size must be greater than 0.");
        auto O3DPointCloud = this->Cvt2O3DPointCloud();
        auto O3DPointCloudDown = O3DPointCloud->VoxelDownSample(voxelSize);
        this->Points.clear();
        for (auto &point : O3DPointCloudDown->points_)
            this->Points.push_back(point);
        this->Colors.clear();
        for (auto &color : O3DPointCloudDown->colors_)
            this->Colors.push_back(color);
        this->Normals.clear();
        for (auto &normal : O3DPointCloudDown->normals_)
            this->Normals.push_back(normal);
    }

    void DFPointCloud::ApplyColor(const Eigen::Vector3d &color)
    {
        this->Colors.clear();
        for (auto &point : this->Points)
            this->Colors.push_back(color);
    }
    void DFPointCloud::ApplyColor(int r, int g, int b)
    {
        Eigen::Vector3d color = Eigen::Vector3d(r / 255.0, g / 255.0, b / 255.0);
        this->ApplyColor(color);
    }

    void DFPointCloud::RemoveStatisticalOutliers(int nbNeighbors, double stdRatio)
    {
        std::shared_ptr<open3d::geometry::PointCloud> O3DPointCloud = this->Cvt2O3DPointCloud();
        std::tuple<std::shared_ptr<open3d::geometry::PointCloud>, std::vector<size_t>> returnedTuple = O3DPointCloud->RemoveStatisticalOutliers(nbNeighbors, stdRatio);
        std::shared_ptr<open3d::geometry::PointCloud> O3DPointCloudWithoutOutliers = std::get<0>(returnedTuple);
        this->Points.clear();
        for (auto &point : O3DPointCloudWithoutOutliers->points_)
            this->Points.push_back(point);
        this->Colors.clear();
        for (auto &color : O3DPointCloudWithoutOutliers->colors_)
            this->Colors.push_back(color);
        this->Normals.clear();
        for (auto &normal : O3DPointCloudWithoutOutliers->normals_)
            this->Normals.push_back(normal);
    }

    void DFPointCloud::UniformDownsample(int everyKPoints)
    {
        auto O3DPointCloud = this->Cvt2O3DPointCloud();
        auto O3DPointCloudDown = O3DPointCloud->UniformDownSample(everyKPoints);
        this->Points.clear();
        for (auto &point : O3DPointCloudDown->points_)
            this->Points.push_back(point);
        this->Colors.clear();
        for (auto &color : O3DPointCloudDown->colors_)
            this->Colors.push_back(color);
        this->Normals.clear();
        for (auto &normal : O3DPointCloudDown->normals_)
            this->Normals.push_back(normal);
    }

    void DFPointCloud::DownsampleBySize(int targetSize)
    {
        // get the number of points and confront it with the targetSize and find the corresponding ratio (0 to 1) to downsample
        int numPoints = this->Points.size();
        if (numPoints <= targetSize)
            throw std::invalid_argument("The target size must be smaller than the number of points in the cloud.");
        double ratio = (double)targetSize / (double)numPoints;
        auto O3DPointCloud = this->Cvt2O3DPointCloud();
        auto O3DPointCloudDown = O3DPointCloud->RandomDownSample(ratio);
        this->Points.clear();
        for (auto &point : O3DPointCloudDown->points_)
            this->Points.push_back(point);
        this->Colors.clear();
        for (auto &color : O3DPointCloudDown->colors_)
            this->Colors.push_back(color);
        this->Normals.clear();
        for (auto &normal : O3DPointCloudDown->normals_)
            this->Normals.push_back(normal);
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

    void DFPointCloud::SaveToPLY(const std::string &path)
    {
        auto cloud_ptr = std::make_shared<DFPointCloud>(this->Points, this->Colors, this->Normals);
        diffCheck::io::WritePLYPointCloud(cloud_ptr, path);
    }

    std::vector<double> DFPointCloud::ComputeDistance(std::shared_ptr<geometry::DFPointCloud> target)
    {
        std::vector<double> errors;
        auto O3DSourcePointCloud = this->Cvt2O3DPointCloud();
        auto O3DTargetPointCloud = target->Cvt2O3DPointCloud();
        
        std::vector<double> distances;

        distances = O3DSourcePointCloud->ComputePointCloudDistance(*O3DTargetPointCloud);
        return distances;
    }

    void DFPointCloud::AddPoints(const DFPointCloud &pointCloud)
    {
        this->Points.insert(this->Points.end(), pointCloud.Points.begin(), pointCloud.Points.end());
        this->Colors.insert(this->Colors.end(), pointCloud.Colors.begin(), pointCloud.Colors.end());
        this->Normals.insert(this->Normals.end(), pointCloud.Normals.begin(), pointCloud.Normals.end());
    }

    Eigen::Vector3d DFPointCloud::GetCenterPoint()
    {
        if (this->Points.size() == 0)
            throw std::invalid_argument("The point cloud is empty.");
        Eigen::Vector3d center = Eigen::Vector3d::Zero();
        for (auto &point : this->Points)
            center += point;
        center /= this->Points.size();
        return center;
    }
}
