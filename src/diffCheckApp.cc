
// #include "diffCheck.hh"

#include <open3d/Open3D.h>
#include <open3d/io/PointCloudIO.h>
#include <open3d/io/TriangleMeshIO.h>
#include <open3d/visualization/visualizer/Visualizer.h>

#include <iostream>


int main()
{
  // std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr = std::make_shared<diffCheck::geometry::DFPointCloud>();
  // std::shared_ptr<diffCheck::geometry::DFMesh> dfMeshPtr = std::make_shared<diffCheck::geometry::DFMesh>();
  
  // std::string pathCloud = R"(C:\Users\andre\Downloads\scan_data_normals.ply\scan_data_normals.ply)";
  // std::string pathMesh = R"(F:\diffCheck\temp\export_meesh_tri.ply)";
  // std::string pathMesh = R"(F:\diffCheck\temp\03_mesh.ply)";
  std::string pathMesh = R"(C:\Users\andre\Downloads\crankshaft-hd-ply\Crankshaft HD.ply)";







  // std::shared_ptr<open3d::geometry::TriangleMesh> sphereMesh = open3d::io::CreateMeshFromFile(pathMesh);
  std::shared_ptr<open3d::geometry::TriangleMesh> sphereMesh = open3d::geometry::TriangleMesh::CreateSphere(1.0, 100, 100);
  // // fill the mesh with data
  // sphereMesh->vertices_.clear();
  // sphereMesh->triangles_.clear();

  // dfMeshPtr->LoadFromOpen3DTriangleMesh(sphereMesh);


  // if (!sphereMesh) {
  //   std::cerr << "Failed to create box" << std::endl;
  //   return 1;
  // }

  std::cout << "Number of vertices in the mesh: " << sphereMesh->vertices_.size() << std::endl;
  std::cout << "Number of faces in the mesh: " << sphereMesh->triangles_.size() << std::endl;
  
  std::cout << "Loading mesh from: " << pathMesh << std::endl;

  open3d::visualization::DrawGeometries({sphereMesh});
  


  
  // // dfMeshPtr->Cvt2DFMesh(sphereMesh);

  // // dfPointCloudPtr->LoadFromPLY(pathCloud);
  // // dfMeshPtr->LoadFromPLY(pathMesh);

  // // std::cout << "Number of points in the point cloud: " << dfPointCloudPtr->GetNumPoints() << std::endl;
  // // std::cout << "Number of colors in the point cloud: " << dfPointCloudPtr->GetNumColors() << std::endl;
  // // std::cout << "Number of normals in the point cloud: " << dfPointCloudPtr->GetNumNormals() << std::endl;

  // std::cout << "Number of vertices in the mesh: " << dfMeshPtr->GetNumVertices() << std::endl;
  // std::cout << "Number of faces in the mesh: " << dfMeshPtr->GetNumFaces() << std::endl;
  // std::cout << "Number of normals in the mesh: " << dfMeshPtr->NormalsVertex.size() << std::endl;
  // std::cout << "Number of colors in the mesh: " << dfMeshPtr->ColorsVertex.size() << std::endl;

  // std::shared_ptr<diffCheck::visualizer::Visualizer> visualizerPtr = std::make_shared<diffCheck::visualizer::Visualizer>();
  // // visualizerPtr->AddPointCloud(dfPointCloudPtr);
  // visualizerPtr->AddMesh(dfMeshPtr);
  // visualizerPtr->Run();




  return 0;
}