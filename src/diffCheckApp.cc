
#include "diffCheck.hh"

#include <open3d/Open3D.h>
#include <open3d/io/PointCloudIO.h>
#include <open3d/io/TriangleMeshIO.h>
#include <open3d/visualization/visualizer/Visualizer.h>

#include <iostream>


int main()
{
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFMesh> dfMeshPtr = std::make_shared<diffCheck::geometry::DFMesh>();

  std::string pathCloud = R"(C:\Users\andre\Downloads\scan_data_normals.ply\scan_data_normals.ply)";
  // std::string pathMesh = R"(F:\diffCheck\temp\export_meesh_tri.ply)";
  // std::string pathMesh = R"(F:\diffCheck\temp\03_mesh.ply)";
  std::string pathMesh = R"(C:\Users\andre\Downloads\crankshaft-hd-ply\Crankshaft HD.ply)";

  dfPointCloudPtr->LoadFromPLY(pathCloud);


  std::shared_ptr<open3d::geometry::TriangleMesh> sphereMesh = open3d::geometry::TriangleMesh::CreateSphere(50.0, 100, 100);

  dfMeshPtr->Cvt2DFMesh(sphereMesh);

  std::cout << "Number of vertices in the mesh: " << sphereMesh->vertices_.size() << std::endl;
  std::cout << "Number of faces in the mesh: " << sphereMesh->triangles_.size() << std::endl;

  std::cout << "Loading mesh from: " << pathMesh << std::endl;

  std::shared_ptr<diffCheck::visualizer::Visualizer> vis = std::make_shared<diffCheck::visualizer::Visualizer>();
  vis->AddPointCloud(dfPointCloudPtr);
  vis->AddMesh(dfMeshPtr);
  vis->Run();

  return 0;
}