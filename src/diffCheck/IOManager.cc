#include "IOManager.hh"

#include <open3d/Open3D.h>

#include <CGAL/Simple_cartesian.h>
#include <CGAL/Polyhedron_3.h>
#include <CGAL/IO/PLY/PLY_reader.h>

typedef CGAL::Simple_cartesian<double> Kernel;
typedef CGAL::Polyhedron_3<Kernel> Polyhedron;


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
        
        // bool isFromRhino = false;
        // std::ifstream file(filename);
        // std::string line;
        // while (std::getline(file, line))
        // {
        //     if (line.find("Rhinoeros") != std::string::npos)
        //     {
        //         isFromRhino = true;
        //         break;
        //     }
        // }
        // file.close();
        // std::cout << "isFromRhino: " << isFromRhino << std::endl;


        // bool isFixedLength = false;  // aka Rhino quad/tri exported mesh
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

        return mesh;
    }
} // namespace diffCheck::io