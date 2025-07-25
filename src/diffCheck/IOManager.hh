#pragma once

#include <string>
#include <filesystem>


#include "diffCheck/geometry/DFPointCloud.hh"
#include "diffCheck/geometry/DFMesh.hh"

namespace diffCheck::io
{
    /**
     * @brief Read a point cloud from a file
     * 
     * @param filename the path to the file with the extension
     * @return std::shared_ptr<diffCheck::geometry::DFPointCloud> the point cloud
     */
    std::shared_ptr<diffCheck::geometry::DFPointCloud> ReadPLYPointCloud(const std::string &filename);
    
    /**
     * @brief Read mesh from ply format
     * 
     * @param filename the path to the file with the extension
     * @return std::shared_ptr<diffCheck::geometry::DFMesh> the mesh
     */
    std::shared_ptr<diffCheck::geometry::DFMesh> ReadPLYMeshFromFile(const std::string &filename);

    /**
     * @brief Write a point cloud to a file as a PLY
     * 
     * @param pointCloud the point cloud to write
     * @param filename the path to the file with the extension
     */
    void WritePLYPointCloud(const std::shared_ptr<diffCheck::geometry::DFPointCloud> &pointCloud, const std::string &filename);

    //////////////////////////////////////////////////////////////////////////
    // IO for test suite and tests data
    //////////////////////////////////////////////////////////////////////////
    /// @brief Get the directory where test data is stored
    std::string GetTestDataDir();
    /// @brief Get the path to the roof quarter ply test file
    std::string GetRoofQuarterPlyPath();
    /// @brief Get the path to the plane point cloud with one outlier
    std::string GetPlanePCWithOneOutliers();
    /// @brief Get the path to the Stanford bunny point cloud
    std::string GetBunnyPlyPath();
} // namespace diffCheck::io