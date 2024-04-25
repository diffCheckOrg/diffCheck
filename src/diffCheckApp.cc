
#include "diffCheck.hh"

#include <iostream>
#include <fstream>


int main()
{
  // import clouds
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrGroundTruthNoNormals = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrGroundTruth = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFMesh> dfMeshPtr = std::make_shared<diffCheck::geometry::DFMesh>();

  std::string pathCloud = R"(C:\Users\localuser\Downloads\04_pt.ply)";
  std::string pathMesh = R"(C:\Users\localuser\Downloads\04_mesh.ply)";

  dfMeshPtr->LoadFromPLY(pathMesh);
  dfPointCloudPtr->LoadFromPLY(pathCloud);
  // add noise to dfPointCloudPtr
  for (int i = 0; i < dfPointCloudPtr->Points.size(); i++)
  {
    dfPointCloudPtr->Points[i] += Eigen::Vector3d::Random() * 0.01 ;
  }

  // populate the mesh with points and store it in dfPointCloudPtrGroundTruth
  dfPointCloudPtrGroundTruthNoNormals->Cvt2DFPointCloud(dfMeshPtr->Cvt2O3DTriangleMesh()->SamplePointsUniformly(1000));
  std::shared_ptr<open3d::geometry::PointCloud> pcd = dfPointCloudPtrGroundTruthNoNormals->Cvt2O3DPointCloud();
  pcd->EstimateNormals();
  dfPointCloudPtrGroundTruth->Cvt2DFPointCloud(pcd);

  // create a rigid rotation matrix
  Eigen::Matrix4d T = Eigen::Matrix4d::Identity();
  T.block<3, 3>(0, 0) = Eigen::AngleAxisd(3, Eigen::Vector3d::UnitX()).toRotationMatrix();
  T(0, 3) = 50;
  T(1, 3) = -100;
  T(2, 3) = 100;
  dfPointCloudPtr->ApplyTransformation(diffCheck::transformation::DFTransformation(T));
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrCopy = std::make_shared<diffCheck::geometry::DFPointCloud>(*dfPointCloudPtr);

  // test global registrations Fast and RANSAC-based
  std::vector<diffCheck::transformation::DFTransformation> registrationResults;
  diffCheck::transformation::DFTransformation transformationA =
    diffCheck::registrations::DFGlobalRegistrations::O3DFastGlobalRegistrationFeatureMatching(dfPointCloudPtr, dfPointCloudPtrGroundTruth, true, 0.01, 1, 50, 1, 500, 500);
  std::cout << "Fast transformation: " << transformationA.TransformationMatrix << std::flush;
  dfPointCloudPtr->ApplyTransformation(transformationA);
  registrationResults.push_back(transformationA);
  diffCheck::transformation::DFTransformation transformationB =
    diffCheck::registrations::DFGlobalRegistrations::O3DRansacOnFeatureMatching(dfPointCloudPtrCopy, dfPointCloudPtrGroundTruth);
  std::cout << "Ransac transformation: " << transformationB.TransformationMatrix << std::endl;
  dfPointCloudPtrCopy->ApplyTransformation(transformationB);
  registrationResults.push_back(transformationB);

  // visualize cloud
  std::shared_ptr<diffCheck::visualizer::Visualizer> visualizer = std::make_shared<diffCheck::visualizer::Visualizer>();
  visualizer->AddPointCloud(dfPointCloudPtr);
  visualizer->AddPointCloud(dfPointCloudPtrCopy);
  visualizer->AddMesh(dfMeshPtr);
  visualizer->Run();

  return 0;
}