
#include "diffCheck.hh"

#include <iostream>
#include <fstream>


int main()
{
  // import clouds
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrGroundTruth = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrGroundTruthFromMesh = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFMesh> dfMeshPtr = std::make_shared<diffCheck::geometry::DFMesh>();

  std::string pathCloud = R"(C:\Users\localuser\Downloads\00_pt.ply)";
  std::string pathMesh = R"(C:\Users\localuser\Downloads\00_mesh.ply)";

  dfMeshPtr->LoadFromPLY(pathMesh);
  dfPointCloudPtr->LoadFromPLY(pathCloud);
  dfPointCloudPtrGroundTruth->LoadFromPLY(pathCloud);

  // add noise to dfPointCloudPtr
  std::vector<Eigen::Vector3d> boundingBoxPoints = dfPointCloudPtr->ComputeBoundingBox();
  double meanInterval = (boundingBoxPoints[0] - boundingBoxPoints[1]).norm();
  for (int i = 0; i < dfPointCloudPtr->Points.size(); i++)
  {
    dfPointCloudPtr->Points[i] += Eigen::Vector3d::Random() * 0.002 * meanInterval;
  }
  
  // populate the mesh with points and store it in dfPointCloudPtrGroundTruthFromMesh
  std::shared_ptr<open3d::geometry::PointCloud> pcd_1 = dfMeshPtr->Cvt2O3DTriangleMesh()->SamplePointsUniformly(50000);
  dfPointCloudPtrGroundTruthFromMesh->Cvt2DFPointCloud(pcd_1);

  // create a rigid rotation matrix
  Eigen::Matrix4d T = Eigen::Matrix4d::Identity();
  T.block<3, 3>(0, 0) = Eigen::AngleAxisd(1.57, Eigen::Vector3d::UnitX()).toRotationMatrix();
  T(0, 3) = 5;
  T(1, 3) = -10;
  T(2, 3) = 10;
  dfPointCloudPtr->ApplyTransformation(diffCheck::transformation::DFTransformation(T));

  // create a copy of the point cloud so we can test both global registrations
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrCopy = std::make_shared<diffCheck::geometry::DFPointCloud>(*dfPointCloudPtr);

  // test global registrations Fast and RANSAC-based
  std::vector<diffCheck::transformation::DFTransformation> registrationResults;
  diffCheck::transformation::DFTransformation transformationA =
    diffCheck::registrations::DFGlobalRegistrations::O3DFastGlobalRegistrationFeatureMatching(dfPointCloudPtr, dfPointCloudPtrGroundTruth);
  std::cout << "Fast transformation: " << transformationA.TransformationMatrix << std::endl;
  dfPointCloudPtr->ApplyTransformation(transformationA);
  registrationResults.push_back(transformationA);
  diffCheck::transformation::DFTransformation transformationB =
    diffCheck::registrations::DFGlobalRegistrations::O3DRansacOnFeatureMatching(dfPointCloudPtrCopy, dfPointCloudPtrGroundTruthFromMesh);
  std::cout << "Ransac transformation: " << transformationB.TransformationMatrix << std::endl;
  dfPointCloudPtrCopy->ApplyTransformation(transformationB);
  registrationResults.push_back(transformationB);

  // visualize cloud
  std::shared_ptr<diffCheck::visualizer::Visualizer> visualizer = std::make_shared<diffCheck::visualizer::Visualizer>();
  visualizer->AddPointCloud(dfPointCloudPtrCopy);
  visualizer->AddPointCloud(dfPointCloudPtr);
  visualizer->AddMesh(dfMeshPtr);
  visualizer->Run();

  return 0;
}