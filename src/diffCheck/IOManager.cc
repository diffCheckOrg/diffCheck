#include "IOManager.hh"

#include <open3d/Open3D.h>


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
        std::shared_ptr<open3d::geometry::TriangleMesh> open3dMesh = open3d::io::CreateMeshFromFile(filename);
        std::shared_ptr<diffCheck::geometry::DFMesh> mesh = std::make_shared<diffCheck::geometry::DFMesh>();
        mesh->Cvt2DFMesh(open3dMesh);
        return mesh;

        // FIXME: test if the variable length in open3d is working
        // // check if the ply is from Rhino by searching for the string "Rhinoceros"
        // std::ifstream file(filename);
        // std::string line;
        // bool isRhino = false;
        // while (std::getline(file, line))
        // {
        //     if (line.find("Rhinoceros") != std::string::npos)
        //     {
        //         isRhino = true;
        //         break;
        //     }
        // }
        // file.close();
        // std::cout << "isRhino: " << isRhino << std::endl;

        // // detect if the ply is of fixed variable lengths or not
        // bool isFixedLength = false;
        // std::ifstream file2(filename);
        // std::string line2;
        // while (std::getline(file2, line2))
        // {
        //     if (line2.find("element vertex") != std::string::npos)
        //     {
        //         isFixedLength = true;
        //         break;
        //     }
        // }
        // file2.close();
        // std::cout << "isFixedLength: " << isFixedLength << std::endl;
    }
} // namespace diffCheck::io