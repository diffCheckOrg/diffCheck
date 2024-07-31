#include "IOManager.hh"

#include <open3d/Open3D.h>

#include "diffCheck/log.hh"

#include <cstdlib>
#include <filesystem>
#include <iostream>
#include <fstream>

namespace diffCheck::io
{
    std::shared_ptr<diffCheck::geometry::DFPointCloud> ReadPLYPointCloud(const std::string &filename)
    {
        std::shared_ptr<open3d::geometry::PointCloud> open3dPointCloud = open3d::io::CreatePointCloudFromFile(filename);
        std::shared_ptr<diffCheck::geometry::DFPointCloud> pointCloud = std::make_shared<diffCheck::geometry::DFPointCloud>();
        pointCloud->Cvt2DFPointCloud(open3dPointCloud);
        return pointCloud;
    }

    std::shared_ptr<diffCheck::geometry::DFMesh> ReadPLYMeshFromFile(const std::string &filename)
    {
        std::shared_ptr<diffCheck::geometry::DFMesh> mesh = std::make_shared<diffCheck::geometry::DFMesh>();
        std::shared_ptr<open3d::geometry::TriangleMesh> open3dMesh = open3d::io::CreateMeshFromFile(filename);
        mesh->Cvt2DFMesh(open3dMesh);

        return mesh;
    }

    std::string GetTestDataDir()
    {
        // for github action conviniency
        const char* env_p = std::getenv("DF_TEST_DATA_DIR");
        std::filesystem::path pathTestData;
        if (env_p != nullptr)
        {
            pathTestData = std::filesystem::path(env_p);
        }
        else
        {
            std::filesystem::path path = std::filesystem::path(__FILE__).parent_path().parent_path().parent_path();
            pathTestData = path / "tests" / "test_data";
        }
        pathTestData = std::filesystem::absolute(pathTestData);
        return pathTestData.string();
    }

    std::string GetRoofQuarterPlyPath()
    {
        std::filesystem::path pathTestData = GetTestDataDir();
        std::filesystem::path pathCloud = pathTestData / "roof_quarter.ply";
        return pathCloud.string();
    }
} // namespace diffCheck::io