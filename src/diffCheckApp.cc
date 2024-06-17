#include "diffCheck.hh"

#include <iostream>
#include <fstream>

#include <open3d/Open3D.h>
// #include <open3d/t/geometry/RaycastingScene.h>

int main()
{
  // import clouds
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr 
      = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFMesh> dfMeshPtr 
      = std::make_shared<diffCheck::geometry::DFMesh>();

  // create a sphere from o3d
  std::string pathCloud = R"(C:\Users\andre\Downloads\moved_04.ply)";
  std::string pathMesh = R"(C:\Users\andre\Downloads\meshtest.ply)";

  dfPointCloudPtr->LoadFromPLY(pathCloud);
  dfMeshPtr->LoadFromPLY(pathMesh);

  open3d::geometry::TriangleMesh meshO3d = *dfMeshPtr->Cvt2O3DTriangleMesh();
  open3d::geometry::PointCloud pointCloudO3d = *dfPointCloudPtr->Cvt2O3DPointCloud();

  auto rayCastingScene = open3d::t::geometry::RaycastingScene();
  // Get the vertices of the mesh
  std::vector<Eigen::Vector3d> vertices = meshO3d.vertices_;

  // Convert the vertices to a tensor
  std::vector<float> verticesPosition;
  for (const auto& vertex : vertices) {
      verticesPosition.insert(verticesPosition.end(), vertex.data(), vertex.data() + 3);
  }
  open3d::core::Tensor verticesPositionTensor(verticesPosition.data(), {static_cast<int64_t>(vertices.size()), 3}, open3d::core::Dtype::Float32);

  std::vector<uint32_t> triangles;
  for (int i = 0; i < meshO3d.triangles_.size(); i++) {
      triangles.push_back(static_cast<uint32_t>(meshO3d.triangles_[i].x()));
      triangles.push_back(static_cast<uint32_t>(meshO3d.triangles_[i].y()));
      triangles.push_back(static_cast<uint32_t>(meshO3d.triangles_[i].z()));
  }
  open3d::core::Tensor trianglesTensor(triangles.data(), {static_cast<int64_t>(meshO3d.triangles_.size()), 3}, open3d::core::Dtype::UInt32);
  
  rayCastingScene.AddTriangles(verticesPositionTensor, trianglesTensor);

  // compute the cloud to mesh signed distance
  std::vector<float> cloudPoints;
  for (const auto& point : pointCloudO3d.points_) {
      cloudPoints.insert(cloudPoints.end(), point.data(), point.data() + 3);
  }
  open3d::core::Tensor cloudPointsTensor(cloudPoints.data(), {static_cast<int64_t>(pointCloudO3d.points_.size()), 3}, open3d::core::Dtype::Float32);


  open3d::core::Tensor sdf = rayCastingScene.ComputeSignedDistance(cloudPointsTensor);

  // if true, get the absolute value of the sdf
  if (true) {
      sdf = sdf.Abs();
  }

  // convert sdf to a vector
  std::vector<float> sdfVector(sdf.GetDataPtr<float>(), sdf.GetDataPtr<float>() + sdf.NumElements());


  // >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  // compute point cloud to point cloud distance
  auto distances = dfPointCloudPtr->ComputeP2PDistance(dfPointCloudPtr);
  for (auto &dist : distances)
  {
    std::cout << dist << std::endl;
  }



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