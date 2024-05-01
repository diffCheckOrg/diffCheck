
#include "diffCheck.hh"

#include <iostream>
#include <fstream>

#include <Eigen/Core>
#include <Open3D/Open3D.h>

int main()
{
  std::vector<Eigen::Vector3d> points;
  std::vector<Eigen::Vector3d> normals;
  std::vector<Eigen::Vector3d> colors;
  points.push_back(Eigen::Vector3d(0, 0, 0));
  points.push_back(Eigen::Vector3d(1, 0, 0));
  points.push_back(Eigen::Vector3d(0, 1, 0));

  normals.push_back(Eigen::Vector3d(0, 0, 1));
  normals.push_back(Eigen::Vector3d(0, 0, 1));
  normals.push_back(Eigen::Vector3d(0, 0, 1));

  colors.push_back(Eigen::Vector3d(1, 0, 0));
  colors.push_back(Eigen::Vector3d(0, 1, 0));
  colors.push_back(Eigen::Vector3d(0, 0, 1));

  diffCheck::geometry::DFPointCloud dfPointCloud(points, colors, normals);

  DIFFCHECK_INFO("Starting diffCheckApp...");

  // create a sphere from o3d
  auto mesh = open3d::geometry::TriangleMesh::CreateSphere(1.0, 4);
  std::shared_ptr<diffCheck::geometry::DFMesh> dfMeshPtr = std::make_shared<diffCheck::geometry::DFMesh>();
  dfMeshPtr->Cvt2DFMesh(mesh);

  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr = std::make_shared<diffCheck::geometry::DFPointCloud>();
  dfPointCloudPtr = dfMeshPtr->SamplePointsUniformly(1000);

  // visualize cloud
  std::shared_ptr<diffCheck::visualizer::Visualizer> visualizer = std::make_shared<diffCheck::visualizer::Visualizer>();
  visualizer->AddPointCloud(dfPointCloudPtr);
  visualizer->Run();





  // // import clouds
  // std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr = std::make_shared<diffCheck::geometry::DFPointCloud>();
  // std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr_1 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  // std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr_2 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  // std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrWithoutNormals = std::make_shared<diffCheck::geometry::DFPointCloud>();
  // std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrGroundTruth = std::make_shared<diffCheck::geometry::DFPointCloud>();
  // std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrGroundTruthFromMesh = std::make_shared<diffCheck::geometry::DFPointCloud>();

  // // std::string pathCloud = R"(C:\Users\andre\Downloads\scan_data_normals.ply\scan_data_normals.ply)";
  // // std::string pathMesh = R"(F:\diffCheck\temp\03_mesh.ply)";

  // // create a sphere from o3d
  // auto mesh = open3d::geometry::TriangleMesh::CreateSphere(1.0, 4);

  // DIFFCHECK_INFO("test");
  // DIFFCHECK_WARN("test");
  // DIFFCHECK_ERROR("test");
  // DIFFCHECK_FATAL("test");
  // std::string pathCloud = R"(C:\Users\localuser\Downloads\04_pt.ply)";
  // std::string pathCloud_1 = R"(C:\Users\localuser\Downloads\part_1_module.ply)";
  // std::string pathCloud_2 = R"(C:\Users\localuser\Downloads\part_2_module.ply)";
  // std::string pathMesh = R"(C:\Users\localuser\Downloads\04_mesh.ply)";

  // dfMeshPtr->LoadFromPLY(pathMesh);
  // dfPointCloudPtr->LoadFromPLY(pathCloud);
  // dfPointCloudPtr_1->LoadFromPLY(pathCloud_1);
  // dfPointCloudPtr_2->LoadFromPLY(pathCloud_2);
  // dfPointCloudPtrGroundTruth->LoadFromPLY(pathCloud);

  // // add noise to dfPointCloudPtr
  // std::vector<Eigen::Vector3d> boundingBoxPoints = dfPointCloudPtr->ComputeBoundingBox();
  // double meanInterval = (boundingBoxPoints[0] - boundingBoxPoints[1]).norm();
  // for (int i = 0; i < dfPointCloudPtr->Points.size(); i++)
  // {
  //   dfPointCloudPtr->Points[i] += Eigen::Vector3d::Random() * 0.002 * meanInterval;
  // }

  // std::shared_ptr<open3d::geometry::PointCloud> pcd_1 = dfPointCloudPtr->Cvt2O3DPointCloud();
  // if (pcd_1->normals_.size() > 0)
  // {
  //   pcd_1->normals_.clear();
  // }
  // dfPointCloudPtrWithoutNormals->Cvt2DFPointCloud(pcd_1);
  
  // // populate the mesh with points and store it in dfPointCloudPtrGroundTruthFromMesh
  // std::shared_ptr<open3d::geometry::PointCloud> pcd_2 = dfMeshPtr->Cvt2O3DTriangleMesh()->SamplePointsUniformly(50000);
  // dfPointCloudPtrGroundTruthFromMesh->Cvt2DFPointCloud(pcd_2);

  // // create a rigid rotation matrix
  // Eigen::Matrix4d T = Eigen::Matrix4d::Identity();
  // T.block<3, 3>(0, 0) = Eigen::AngleAxisd(1.57, Eigen::Vector3d::UnitX()).toRotationMatrix();
  // T(0, 3) = 50;
  // T(1, 3) = -100;
  // T(2, 3) = 100;
  // dfPointCloudPtrWithoutNormals->ApplyTransformation(diffCheck::transformation::DFTransformation(T));

  // // create a copy of the point cloud so we can test both global registrations
  // std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrCopy = std::make_shared<diffCheck::geometry::DFPointCloud>(*dfPointCloudPtrWithoutNormals);

  // // test global registrations Fast and RANSAC-based
  // std::vector<diffCheck::transformation::DFTransformation> registrationResults;
  // diffCheck::transformation::DFTransformation transformationA =
  //   diffCheck::registrations::DFGlobalRegistrations::O3DFastGlobalRegistrationFeatureMatching(dfPointCloudPtr_1, dfPointCloudPtr_2);
  // std::cout << "Fast transformation: " << transformationA.TransformationMatrix << std::endl;
  // //dfPointCloudPtr_1->ApplyTransformation(transformationA);
  // registrationResults.push_back(transformationA);
  // diffCheck::transformation::DFTransformation transformationB =
  //   diffCheck::registrations::DFGlobalRegistrations::O3DRansacOnFeatureMatching(dfPointCloudPtr_1, dfPointCloudPtr_2);
  // std::cout << "Ransac transformation: " << transformationB.TransformationMatrix << std::endl;
  // dfPointCloudPtr_1->ApplyTransformation(transformationB);
  // registrationResults.push_back(transformationB);

  // // visualize cloud
  // std::shared_ptr<diffCheck::visualizer::Visualizer> visualizer = std::make_shared<diffCheck::visualizer::Visualizer>();
  // visualizer->AddPointCloud(dfPointCloudPtr_1);
  // visualizer->AddPointCloud(dfPointCloudPtr_2);
  // // visualizer->AddMesh(dfMeshPtr);
  // visualizer->Run();


  return 0;
}