
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
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrAfterTrans_1 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrAfterTrans_2 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrAfterTrans_3 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrAfterTrans_4 = std::make_shared<diffCheck::geometry::DFPointCloud>();
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
    dfPointCloudPtr->Points[i] += Eigen::Vector3d::Random() * 0.01 ;
  }

  std::vector<double> timesFGRFeatureMatching;
  std::vector<double> timesFGRCorrespondance;
  std::vector<double> timesRansacCorrespondance;
  std::vector<double> timesRansacFeatureMatching;

  std::vector<double> errorsFGRFeatureMatching;
  std::vector<double> errorsFGRCorrespondance;
  std::vector<double> errorsRansacCorrespondance;
  std::vector<double> errorsRansacFeatureMatching;
int iterations = 50;

  // populate the mesh with points and store it in dfPointCloudPtrGroundTruth
  dfPointCloudPtrGroundTruth->Cvt2DFPointCloud(dfMeshPtr->Cvt2O3DTriangleMesh()->SamplePointsUniformly(100000));

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
  dfPointCloudPtrAfterTrans_1 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  dfPointCloudPtrAfterTrans_2 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  dfPointCloudPtrAfterTrans_3 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  dfPointCloudPtrAfterTrans_4 = std::make_shared<diffCheck::geometry::DFPointCloud>();

  dfPointCloudPtrAfterTrans_1->Cvt2DFPointCloud(o3DPointCloudAfterTrans);
  dfPointCloudPtrAfterTrans_2->Cvt2DFPointCloud(o3DPointCloudAfterTrans);
  dfPointCloudPtrAfterTrans_3->Cvt2DFPointCloud(o3DPointCloudAfterTrans);
  dfPointCloudPtrAfterTrans_4->Cvt2DFPointCloud(o3DPointCloudAfterTrans);

  // Testing the Fast Global Registration on Feature Matching method
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrAfterReg_1 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  clock_t start_1 = clock();
  auto result_1 = diffCheck::registration::GlobalRegistration::O3DFastGlobalRegistrationBasedOnCorrespondence(dfPointCloudPtrAfterTrans_1, dfPointCloudPtr);
  double _intermediate_time_1 = (clock() - start_1) / (double) CLOCKS_PER_SEC;
  timesFGRFeatureMatching.push_back(_intermediate_time_1);
  Eigen::Matrix<double, 4, 4> transformation = result_1.transformation_;
  std::shared_ptr<open3d::geometry::PointCloud> o3DPointCloudPtrAfterReg_1 = std::make_shared<open3d::geometry::PointCloud>(dfPointCloudPtrAfterTrans_1->Cvt2O3DPointCloud()->Transform(transformation));
  dfPointCloudPtrAfterReg_1->Cvt2DFPointCloud(o3DPointCloudPtrAfterReg_1);
  std::vector<double> errors_1 =  diffCheck::registration::GlobalRegistration::ComputeP2PDistance(dfPointCloudPtrAfterReg_1, dfPointCloudPtrGroundTruth);
  errorsFGRFeatureMatching.push_back(std::accumulate(errors_1.begin(), errors_1.end(), 0.0) / errors_1.size());

  // Testing the Fast Global Registration on Correspondance method
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrAfterReg_2 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  clock_t start_2 = clock();
  auto result_2 = diffCheck::registration::GlobalRegistration::O3DFastGlobalRegistrationBasedOnCorrespondence(dfPointCloudPtrAfterTrans_2, dfPointCloudPtr);
  double _intermediate_time_2 = (clock() - start_2) / (double) CLOCKS_PER_SEC;
  timesFGRCorrespondance.push_back(_intermediate_time_2);
  Eigen::Matrix<double, 4, 4> transformation_2 = result_2.transformation_;
  std::shared_ptr<open3d::geometry::PointCloud> o3DPointCloudPtrAfterReg_2 = std::make_shared<open3d::geometry::PointCloud>(dfPointCloudPtrAfterTrans_2->Cvt2O3DPointCloud()->Transform(transformation_2));
  dfPointCloudPtrAfterReg_2->Cvt2DFPointCloud(o3DPointCloudPtrAfterReg_2);
  std::vector<double> errors_2 =  diffCheck::registration::GlobalRegistration::ComputeP2PDistance(dfPointCloudPtrAfterReg_2, dfPointCloudPtrGroundTruth);
  errorsFGRCorrespondance.push_back(std::accumulate(errors_2.begin(), errors_2.end(), 0.0) / errors_2.size());

  // Testing the Ransac registration based on correspondance method
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrAfterReg_3 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  clock_t start_3 = clock();
  auto result_3 = diffCheck::registration::GlobalRegistration::O3DRansacOnCorrespondence(dfPointCloudPtrAfterTrans_3, dfPointCloudPtr);
  double _intermediate_time_3 = (clock() - start_3) / (double) CLOCKS_PER_SEC;
  timesRansacCorrespondance.push_back(_intermediate_time_3);
  Eigen::Matrix<double, 4, 4> transformation_3 = result_3.transformation_;
  std::shared_ptr<open3d::geometry::PointCloud> o3DPointCloudPtrAfterReg_3 = std::make_shared<open3d::geometry::PointCloud>(dfPointCloudPtrAfterTrans_3->Cvt2O3DPointCloud()->Transform(transformation_3));
  dfPointCloudPtrAfterReg_3->Cvt2DFPointCloud(o3DPointCloudPtrAfterReg_3);
  std::vector<double> errors_3 = diffCheck::registration::GlobalRegistration::ComputeP2PDistance(dfPointCloudPtrAfterReg_3, dfPointCloudPtrGroundTruth);
  errorsRansacCorrespondance.push_back(std::accumulate(errors_3.begin(), errors_3.end(), 0.0) / errors_3.size());

  // Testing the Ransac registration based on Feature Matching method
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrAfterReg_4 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  clock_t start_4 = clock();
  auto result_4 = diffCheck::registration::GlobalRegistration::O3DRansacOnFeatureMatching(dfPointCloudPtrAfterTrans_4, dfPointCloudPtr);
  double _intermediate_time_4 = (clock() - start_4) / (double) CLOCKS_PER_SEC;
  timesRansacFeatureMatching.push_back(_intermediate_time_4);
  Eigen::Matrix<double, 4, 4> transformation_4 = result_4.transformation_;
  std::shared_ptr<open3d::geometry::PointCloud> o3DPointCloudPtrAfterReg_4 = std::make_shared<open3d::geometry::PointCloud>(dfPointCloudPtrAfterTrans_4->Cvt2O3DPointCloud()->Transform(transformation_4));
  dfPointCloudPtrAfterReg_4->Cvt2DFPointCloud(o3DPointCloudPtrAfterReg_4);
  std::vector<double> errors_4 = diffCheck::registration::GlobalRegistration::ComputeP2PDistance(dfPointCloudPtrAfterReg_4, dfPointCloudPtrGroundTruth);
  errorsRansacFeatureMatching.push_back(std::accumulate(errors_4.begin(), errors_4.end(), 0.0) / errors_4.size());

  std::cout<<"Iteration: "<<i<<" "<<std::flush;

  if(i%10 == 0)
  {
    std::cout<<std::endl;
  
  diffCheck::visualizer::Visualizer devisu = diffCheck::visualizer::Visualizer();
  devisu.AddPointCloud(dfPointCloudPtrAfterReg_1);
  devisu.AddPointCloud(dfPointCloudPtrAfterReg_2);
  devisu.AddPointCloud(dfPointCloudPtrAfterReg_3);
  devisu.AddPointCloud(dfPointCloudPtrAfterReg_4);
  devisu.AddMesh(dfMeshPtr);
  devisu.Run();
  }
  }
  
  // write the errors and computation times to 2 csv files with one column per method
  std::ofstream fileErrors("errors.csv");
  std::ofstream fileTimes("times.csv");
  fileErrors<<"FGR Feature Matching,FGR Correspondance,Ransac Correspondance,Ransac Feature Matching"<<std::endl;
  fileTimes<<"FGR Feature Matching,FGR Correspondance,Ransac Correspondance,Ransac Feature Matching"<<std::endl;
  for (int i = 0; i < transformations.size(); i++)
  {
    fileErrors<<errorsFGRFeatureMatching[i]<<","<<errorsFGRCorrespondance[i]<<","<<errorsRansacCorrespondance[i]<<","<<errorsRansacFeatureMatching[i]<<std::endl;
    fileTimes<<timesFGRFeatureMatching[i]<<","<<timesFGRCorrespondance[i]<<","<<timesRansacCorrespondance[i]<<","<<timesRansacFeatureMatching[i]<<std::endl;
  }
  fileErrors.close();
  fileTimes.close();
  return 0;
}