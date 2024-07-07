#include "diffCheck.hh"

#include <iostream>
#include <fstream>


int main()
{
  // import clouds
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr 
      = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFMesh> dfMeshPtr 
      = std::make_shared<diffCheck::geometry::DFMesh>();

  // // create a sphere from o3d
  // std::string pathCloud = R"(C:\andre\Downloads\moved_04.ply)";
  // std::string pathMesh = R"(C:\Users\andre\Downloads\meshtest.ply)";

  // // dfPointCloudPtr->LoadFromPLY(pathCloud);
  // dfMeshPtr->LoadFromPLY(pathMesh);

  // open3d::geometry::TriangleMesh meshO3d = *dfMeshPtr->Cvt2O3DTriangleMesh();


  // // convert the sphere to a diffCheck point cloud
  // // auto o3dPointCloud = meshO3d.SamplePointsUniformly(1000);

  // std::shared_ptr<open3d::geometry::PointCloud> tightBBOX = std::make_shared<open3d::geometry::PointCloud>();

  // // compute the bounding box
  // open3d::geometry::OrientedBoundingBox bbox = meshO3d.GetMinimalOrientedBoundingBox();
  // std::vector<Eigen::Vector3d> bboxPts = bbox.GetBoxPoints();
  // for (auto &pt : bboxPts)
  // {
  //   tightBBOX->points_.push_back(pt);
  // }


  // dfPointCloudPtr->Cvt2DFPointCloud(tightBBOX);




  // std::shared_ptr<diffCheck::visualizer::Visualizer> vis = std::make_shared<diffCheck::visualizer::Visualizer>();
  // vis->AddPointCloud(dfPointCloudPtr);
  // // vis->AddMesh(dfMeshPtr);
  // vis->Run();


  return 0;
}