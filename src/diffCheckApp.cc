
#include "diffCheck.hh"


int main()
{
  diffCheck::func1();
  diffCheck::func2();
  diffCheck::func3();

  diffCheck::testOpen3d();


  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr = std::make_shared<diffCheck::geometry::DFPointCloud>();
  // std::shared_ptr<open3d::geometry::PointCloud> cloud(new open3d::geometry::PointCloud());

  // // fill the point cloud with random points
  // cloud->points_.resize(100);
  // for (auto &point : cloud->points_) {
  //     point = Eigen::Vector3d::Random();
  // }
  // // set the point cloud color to be light blue
  // cloud->colors_.resize(100);
  // for (auto &color : cloud->colors_) {
  //     color = Eigen::Vector3d(0.7, 0.7, 1.0);
  // }
  // // set the normal of the point cloud
  // cloud->normals_.resize(100);
  // for (auto &normal : cloud->normals_) {
  //     normal = Eigen::Vector3d(0.0, 0.0, 1.0);
  // }

  // dfPointCloudPtr->Cvt2DFPointCloud(cloud);
  std::string path = R"(C:\Users\andre\Downloads\scan_data_normals.ply\scan_data_normals.ply)";

  dfPointCloudPtr->LoadFromPLY(path);

  std::cout << "Number of points in the point cloud: " << dfPointCloudPtr->GetNumPoints() << std::endl;
  std::cout << "Number of colors in the point cloud: " << dfPointCloudPtr->GetNumColors() << std::endl;
  std::cout << "Number of normals in the point cloud: " << dfPointCloudPtr->GetNumNormals() << std::endl;


  std::shared_ptr<diffCheck::visualizer::Visualizer> visualizerPtr = std::make_shared<diffCheck::visualizer::Visualizer>();
  visualizerPtr->LoadPointCloud(dfPointCloudPtr);
  visualizerPtr->Run();

  return 0;
}