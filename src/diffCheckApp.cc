
#include "diffCheck.hh"



int main()
{

  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudFromMeshPtr = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFMesh> dfMeshPtr = std::make_shared<diffCheck::geometry::DFMesh>();

  std::string pathCloud = R"(C:/Users/localuser/Downloads/04_pt.ply)";
  std::string pathRefCloud = R"(C:/Users/localuser/Downloads/04_mesh_ref_pts.ply)";
  std::string pathMesh = R"(C:/Users/localuser/Downloads/04_mesh.ply)";

  std::shared_ptr<open3d::geometry::TriangleMesh> sphere_mesh = open3d::geometry::TriangleMesh::CreateSphere(10, 5, false);

  // Compute vertex normals
  sphere_mesh->ComputeVertexNormals();

  std::cout << " Number of vertices in the mesh: " << sphere_mesh->vertices_.size() << std::endl;
  std::cout << " Number of triangles in the mesh: " << sphere_mesh->triangles_.size() << std::endl;
  std::cout << " Number of triangle normals in the mesh: " << sphere_mesh->triangle_normals_.size() << std::endl;
  std::cout << " Number of vertex normals in the mesh: " << sphere_mesh->vertex_normals_.size() << std::endl;
  
  dfPointCloudPtr->LoadFromPLY(pathCloud);
  dfPointCloudFromMeshPtr->LoadFromPLY(pathRefCloud);
  dfMeshPtr->LoadFromPLY(pathMesh);
  std::shared_ptr<diffCheck::registration::Registration> registrationPtr = std::make_shared<diffCheck::registration::Registration>();
  // registrationPtr->RegisterICPO3D(dfPointCloudPtr, dfPointCloudFromMeshPtr, 0.1);

  // std::cout << "Number of points in the point cloud: " << dfPointCloudPtr->GetNumPoints() << std::endl;
  // std::cout << "Number of colors in the point cloud: " << dfPointCloudPtr->GetNumColors() << std::endl;
  // std::cout << "Number of normals in the point cloud: " << dfPointCloudPtr->GetNumNormals() << std::endl;

  // std::cout << "Number of vertices in the mesh: " << dfMeshPtr->GetNumVertices() << std::endl;
  // std::cout << "Number of faces in the mesh: " << dfMeshPtr->GetNumFaces() << std::endl;
  // std::cout << "Number of normals in the mesh: " << dfMeshPtr->NormalsVertex.size() << std::endl;
  // std::cout << "Number of colors in the mesh: " << dfMeshPtr->ColorsVertex.size() << std::endl;

  std::shared_ptr<diffCheck::visualizer::Visualizer> visualizerPtr = std::make_shared<diffCheck::visualizer::Visualizer>();
  visualizerPtr->AddPointCloud(dfPointCloudPtr);
  visualizerPtr->AddMesh(dfMeshPtr);
  visualizerPtr->Run();

  return 0;
}