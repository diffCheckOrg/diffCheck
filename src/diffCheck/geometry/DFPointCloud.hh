#pragma once

#include <Eigen/Core>
#include <open3d/Open3D.h>


namespace diffCheck::geometry
{
    class DFPointCloud
    {
    public:
        DFPointCloud() = default;
        ~DFPointCloud() = default;

    ///< Converters from other point cloud datatypes libraries to our format
    public:
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

    ///< I/O loader
    public:
        /**
         * @brief Read a point cloud from a file
         * 
         * @param filename the path to the file with the extension
         */
        void LoadFromPLY(const std::string &path);

    ///< Getters
    public:
        /// @brief Number of points in the point cloud
        int GetNumPoints() const { return this->Points.size(); }
        /// @brief Number of colors in the point cloud
        int GetNumColors() const { return this->Colors.size(); }
        /// @brief Number of normals in the point cloud
        int GetNumNormals() const { return this->Normals.size(); }

    ///< Basic point cloud data
    public:
        /// @brief Eigen vector of 3D points
        std::vector<Eigen::Vector3d> Points;
        /// @brief Eigen vector of 3D colors
        std::vector<Eigen::Vector3d> Colors;
        /// @brief Eigen vector of 3D normals
        std::vector<Eigen::Vector3d> Normals;
    };
} // namespace diffCheck::geometry