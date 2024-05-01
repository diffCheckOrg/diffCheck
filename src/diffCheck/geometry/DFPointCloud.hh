#pragma once

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

    public:  ///< Basic point cloud data
        /// @brief Eigen vector of 3D points
        std::vector<Eigen::Vector3d> Points;
        /// @brief Eigen vector of 3D colors
        std::vector<Eigen::Vector3d> Colors;
        /// @brief Eigen vector of 3D normals
        std::vector<Eigen::Vector3d> Normals;
    };
} // namespace diffCheck::geometry