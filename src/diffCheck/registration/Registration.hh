#pragma once

#include <Eigen/Core>
#include <open3d/Open3D.h>
#include <open3d/geometry/TriangleMesh.h>
#include <open3d/geometry/PointCloud.h>
#include <open3d/pipelines/registration/Registration.h>
#include "diffCheck/geometry/DFMesh.hh"
#include "diffCheck/geometry/DFPointCloud.hh"


namespace diffCheck::registration
{
class Registration
{
public:
    Registration() = default;
    ~Registration() = default;

///< Standard registration methods from Open3D
public:

    /**
     * @brief Register two point clouds using ICP
     * 
     * @param source the source point cloud pointer
     * @param target the target point cloud pointer
     * @param threshold the threshold for the ICP algorithm
     */
    void RegisterICPO3D( std::shared_ptr<diffCheck::geometry::DFPointCloud> &source,  std::shared_ptr<diffCheck::geometry::DFPointCloud> &target, double threshold);

///< population of meshes
public:

    /**
     * @brief Populate the mesh with the point cloud
     * 
     * @param mesh the mesh pointer
     * @param pointCloud the point cloud pointer
     */
    void PopulateMesh( std::shared_ptr<diffCheck::geometry::DFMesh> &mesh,  std::shared_ptr<diffCheck::geometry::DFPointCloud> &pointCloud, int numPoints);

};
}