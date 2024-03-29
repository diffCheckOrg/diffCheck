
#include "diffCheck.hh"

#include <iostream>
#include <fstream>


int main()
{
  // import clouds
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr_1 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr_2 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrWithoutNormals = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrGroundTruth = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrGroundTruthFromMesh = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFMesh> dfMeshPtr = std::make_shared<diffCheck::geometry::DFMesh>();

  // std::string pathCloud = R"(C:\Users\andre\Downloads\scan_data_normals.ply\scan_data_normals.ply)";
  // std::string pathMesh = R"(F:\diffCheck\assets\dataset\mesh_fromRh_unfixedLength.ply)";
  // std::string pathMesh = R"(F:\diffCheck\temp\03_mesh.ply)";

  // create a sphere from o3d
  auto mesh = open3d::geometry::TriangleMesh::CreateSphere(1.0, 4);
  dfMeshPtr->LoadFromPLY(pathMesh);


  dfMeshPtr->Cvt2DFMesh(mesh);

  // dfPointCloudPtr->LoadFromPLY(pathCloud);

  std::shared_ptr<diffCheck::visualizer::Visualizer> vis = std::make_shared<diffCheck::visualizer::Visualizer>();
  // vis->AddPointCloud(dfPointCloudPtr);
  vis->AddMesh(dfMeshPtr);
  vis->Run();

  return 0;
}