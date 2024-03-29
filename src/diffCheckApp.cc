
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
  std::string pathMesh = R"(F:\diffCheck\assets\dataset\mesh_fromRh_unfixedLength.ply)";
  // std::string pathMesh = R"(F:\diffCheck\temp\03_mesh.ply)";


  dfMeshPtr->LoadFromPLY(pathMesh);
  // dfPointCloudPtr->LoadFromPLY(pathCloud);

  std::shared_ptr<diffCheck::visualizer::Visualizer> vis = std::make_shared<diffCheck::visualizer::Visualizer>();
  // vis->AddPointCloud(dfPointCloudPtr);
  vis->AddMesh(dfMeshPtr);
  vis->Run();

  return 0;
}