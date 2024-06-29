#pragma once

#include <optional>
#include <Eigen/Core>
#include <open3d/Open3D.h>

#include <diffCheck/transformation/DFTransformation.hh>


namespace diffCheck::geometry
{
    class DFPointCloud
    {
    public:
        DFPointCloud() {}
        DFPointCloud(std::vector<Eigen::Vector3d> points,
                     std::vector<Eigen::Vector3d> colors,
                     std::vector<Eigen::Vector3d> normals)
            : Points(points), Colors(colors), Normals(normals) 
        {}
        
        ~DFPointCloud() = default;

    
    public:  ///< Converters from other point cloud datatypes libraries to our format
        /**
         * @brief Converter from open3d point cloud to our datatype
         * 
         * @param pointCloud the open3d point cloud
         */
        void Cvt2DFPointCloud(const std::shared_ptr<open3d::geometry::PointCloud> &O3DPointCloud);
        
        /**
         * @brief Convert the DFPointCloud to open3d point cloud
         * 
         * @return std::shared_ptr<open3d::geometry::PointCloud> the open3d point cloud
         */
        std::shared_ptr<open3d::geometry::PointCloud> Cvt2O3DPointCloud();

    public:  ///< Utilities
        /** 
        * @brief Compute the "point to point" distance between this and another point clouds. 
        * 
        * For every point in the source point cloud, it looks in the KDTree of the target point cloud and finds the closest point.
        * It returns a vector of distances, one for each point in the source point cloud.
        * 
        * @param target The target diffCheck point cloud
        * @return std::vector<double> A vector of distances, one for each point in the source point cloud.
        * 
        * @see https://github.com/isl-org/Open3D/blob/main/cpp/open3d/geometry/PointCloud.cpp
        */
        std::vector<double> ComputeP2PDistance(std::shared_ptr<geometry::DFPointCloud> target);

        /**
         * @brief Compute the bounding box of the point cloud and stores it as member of the DFPointCloud object
         * 
         * @return std::vector<Eigen::Vector3d> A vector of two Eigen::Vector3d, with the first one being the minimum
         *  point and the second one the maximum point of the bounding box.
        */
        std::vector<Eigen::Vector3d> ComputeBoundingBox();

        /**
         * @brief Estimate the normals of the point cloud by either knn or if the radius
         * is provided by hybrid search.
         * 
         * <a href=https://www.open3d.org/html/cpp_api/classopen3d_1_1t_1_1geometry_1_1_point_cloud.html#a4937528c4b6194092631f002bccc44d0> Reference from Open3d</a>.
         * @param knn the number of nearest neighbors to consider (by default 30)
         * @param searchRadius the radius of the search, by default deactivated
         */
        void EstimateNormals(
            std::optional<int> knn = 30,
            std::optional<double> searchRadius = std::nullopt);

    public:  ///< Downsamplers
        /**
         * @brief Downsample the point cloud with voxel grid
         * 
         * @param voxelSize the size of the voxel grid
         */
        void VoxelDownsample(double voxelSize);

        /**
         * @brief Downsample uniformly the point cloud
         * 
         * @param everyKPoints the index of the points to delete
         */
        void UniformDownsample(int everyKPoints);

        /**
         * @brief Downsample a cloud by a size target
         * 
         * @param targetSize the target size of the cloud
         */
        
        void DownsampleBySize(int targetSize);
        /**
         * @brief Get the tight bounding box of the point cloud
         * 
         * @return std::vector<Eigen::Vector3d> A vector of two Eigen::Vector3d, with the first one being the minimum
         * point and the second one the maximum point of the bounding box.
         *  ///      ------- x
         *  ///     /|
         *  ///    / |
         *  ///   /  | z
         *  ///  y
         *  ///      0 ------------------- 1
         *  ///       /|                /|
         *  ///      / |               / |
         *  ///     /  |              /  |
         *  ///    /   |             /   |
         *  /// 2 ------------------- 7  |
         *  ///   |    |____________|____| 6
         *  ///   |   /3            |   /
         *  ///   |  /              |  /
         *  ///   | /               | /
         *  ///   |/                |/
         *  /// 5 ------------------- 4
         *  /// 
        */
        std::vector<Eigen::Vector3d> GetTightBoundingBox();

    public:  ///< Transformers
        /**
         * @brief Apply a transformation to the point cloud
         * 
         * @param transformation the transformation to apply
         */
        void ApplyTransformation(const diffCheck::transformation::DFTransformation &transformation);

    public:  ///< I/O loader
        /**
         * @brief Read a point cloud from a file
         * 
         * @param filename the path to the file with the extension
         */
        void LoadFromPLY(const std::string &path);

    public:  ///< Getters
        /// @brief Number of points in the point cloud
        int GetNumPoints() const { return this->Points.size(); }
        /// @brief Number of colors in the point cloud
        int GetNumColors() const { return this->Colors.size(); }
        /// @brief Number of normals in the point cloud
        int GetNumNormals() const { return this->Normals.size(); }
        /// @brief Get the center point of the point cloud
        Eigen::Vector3d GetCenterPoint();

        /// @brief Check if the cloud has points
        bool HasPoints() const { return this->Points.size() > 0; }
        /// @brief Check if the cloud has colors
        bool HasColors() const { return this->Colors.size() > 0; }
        /// @brief Check if the cloud has normals
        bool HasNormals() const { return this->Normals.size() > 0; }

    public:  ///< Basic point cloud data
        /// @brief Eigen vector of 3D points
        std::vector<Eigen::Vector3d> Points;
        /// @brief Eigen vector of 3D colors
        std::vector<Eigen::Vector3d> Colors;
        /// @brief Eigen vector of 3D normals
        std::vector<Eigen::Vector3d> Normals;
    };
} // namespace diffCheck::geometry