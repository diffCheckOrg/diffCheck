#pragma once

#include <string>
#include <filesystem>

#include <igl/readPLY.h>

#include "diffCheck/geometry/DFPointCloud.hh"

namespace diffCheck::io
{
    /**
     * @brief Read a point cloud from a file
     * 
     * @param filename the path to the file with the extension
     */
    std::shared_ptr<diffCheck::geometry::DFPointCloud> ReadPLYPointCloud(const std::string &filename);
    
    // TODO: return a dggeometry::Mesh object
    /**
     * @brief Read mesh of format file
     * 
     * @param filename the path to the file with the extension
     */
    void ReadPLYMeshFromFile(const std::string &filename);
} // namespace diffCheck::io