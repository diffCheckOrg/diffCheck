
#include "diffCheck.hh"

#include <open3d/Open3D.h>
#include <open3d/io/PointCloudIO.h>
#include <open3d/io/TriangleMeshIO.h>
#include <open3d/visualization/visualizer/Visualizer.h>

#include <iostream>
#include <time.h>
#include <fstream>


int main()
{
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrAfterTrans = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrGroundTruthNoNormals = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrGroundTruth = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFMesh> dfMeshPtr = std::make_shared<diffCheck::geometry::DFMesh>();

  std::string pathCloud = R"(C:\Users\localuser\Downloads\00_pt.ply)";
  std::string pathMesh = R"(C:\Users\localuser\Downloads\00_mesh.ply)";
  // std::string pathMesh = R"(F:\diffCheck\temp\03_mesh.ply)";

  dfMeshPtr->LoadFromPLY(pathMesh);
  dfPointCloudPtr->LoadFromPLY(pathCloud);

  // add noise to dfPointCloudPtr
  for (int i = 0; i < dfPointCloudPtr->Points.size(); i++)
  {
    dfPointCloudPtr->Points[i] += Eigen::Vector3d::Random() * 0.1 ;
  }

int iterations = 50;

  // populate the mesh with points and store it in dfPointCloudPtrGroundTruth
  dfPointCloudPtrGroundTruthNoNormals->Cvt2DFPointCloud(dfMeshPtr->Cvt2O3DTriangleMesh()->SamplePointsUniformly(10000));
  std::shared_ptr<open3d::geometry::PointCloud> pcd = dfPointCloudPtrGroundTruthNoNormals->Cvt2O3DPointCloud();
  pcd->EstimateNormals();
  dfPointCloudPtrGroundTruth->Cvt2DFPointCloud(pcd);
  std::vector<Eigen::Matrix4d> transformations;
  for (int i = 0; i < iterations; i++)
  {
    // create a rigid rotation matrix
    Eigen::Matrix4d T = Eigen::Matrix4d::Identity();
    T.block<3, 3>(0, 0) = Eigen::AngleAxisd(0.3*i, Eigen::Vector3d::UnitX()).toRotationMatrix();
    T(0, 3) = 30 * i;
    T(1, 3) = -40 * i;
    T(2, 3) = 60 * i;
    transformations.push_back(T);
  }
  
  
  for (int i = 0; i < iterations; i++)
  {
  std::shared_ptr<open3d::geometry::PointCloud> o3DPointCloud = dfPointCloudPtr->Cvt2O3DPointCloud();

  std::shared_ptr<open3d::geometry::PointCloud> o3DPointCloudAfterTrans = std::make_shared<open3d::geometry::PointCloud>(o3DPointCloud->Transform(transformations[i]));
  dfPointCloudPtrAfterTrans = std::make_shared<diffCheck::geometry::DFPointCloud>();
  

  dfPointCloudPtrAfterTrans->Cvt2DFPointCloud(o3DPointCloudAfterTrans);

  std::vector<Eigen::Matrix<double, 4, 4>> registrationResults;
  // Testing the Fast Global Registration on Feature Matching method
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrAfterReg_1 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  diffCheck::transformation::DFTransformation result_1 = diffCheck::registration::GlobalRegistration::O3DFastGlobalRegistrationBasedOnCorrespondence(dfPointCloudPtrAfterTrans, dfPointCloudPtrGroundTruth);
  Eigen::Matrix<double, 4, 4> transformation = result_1.transformationMatrix;
  registrationResults.push_back(transformation);
  
  // Testing the Fast Global Registration on Correspondance method
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrAfterReg_2 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  auto result_2 = diffCheck::registration::GlobalRegistration::O3DFastGlobalRegistrationBasedOnCorrespondence(dfPointCloudPtrAfterTrans, dfPointCloudPtrGroundTruth);
  Eigen::Matrix<double, 4, 4> transformation_2 = result_2.transformationMatrix;
  registrationResults.push_back(transformation_2);  
  
  // Testing the Ransac registration based on correspondance method
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrAfterReg_3 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  auto result_3 = diffCheck::registration::GlobalRegistration::O3DRansacOnCorrespondence(dfPointCloudPtrAfterTrans, dfPointCloudPtrGroundTruth);
  Eigen::Matrix<double, 4, 4> transformation_3 = result_3.transformationMatrix;
  registrationResults.push_back(transformation_3);

  // Testing the Ransac registration based on Feature Matching method
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrAfterReg_4 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  auto result_4 = diffCheck::registration::GlobalRegistration::O3DRansacOnFeatureMatching(dfPointCloudPtrAfterTrans, dfPointCloudPtrGroundTruth);
  Eigen::Matrix<double, 4, 4> transformation_4 = result_4.transformationMatrix;
  registrationResults.push_back(transformation_4);

  std::cout<<"Iteration: "<<i<<" "<<std::flush;
  
  // compute the errors
  std::vector<double> errors = diffCheck::registration::GlobalRegistration::EvaluateRegistrations(dfPointCloudPtrAfterTrans, dfPointCloudPtr, registrationResults);
  std::cout<<"Errors: FGRCorrespondence "<<errors[0]<<", FGRFeatureMatching: "<<errors[1]<<", RanSaC Correspondence: "<<errors[2]<<", RanSaC FeatureMatching: "<<errors[3]<<std::endl;
  }

  return 0;
}