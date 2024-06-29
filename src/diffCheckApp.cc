#include "diffCheck.hh"

#include <iostream>
#include <fstream>

#include <cilantro/utilities/point_cloud.hpp>
#include <cilantro/core/nearest_neighbors.hpp>


int main()
{
  std::shared_ptr<diffCheck::geometry::DFPointCloud> pcdSrc = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::vector<std::shared_ptr<diffCheck::geometry::DFPointCloud>> segments;
  std::string pathPcdSrc = R"(C:\Users\andre\Downloads\moved_04.ply)";

  pcdSrc->LoadFromPLY(pathPcdSrc);

  segments = diffCheck::segmentation::DFSegmentation::NormalBasedSegmentation(
    pcdSrc,
    10.f,
    10,
    true,
    50,
    30,
    true);
  std::cout << "number of segments:" << segments.size()<< std::endl;
  // print the last 5 colors
  for (auto segment : segments)
  {
    for (int i = 0; i < 5; i++)
    {
      std::cout << segment->Colors[i].transpose() << std::endl;
    }
  }

  diffCheck::visualizer::Visualizer vis;
  // vis.AddPointCloud(pcdSrc);
  for (auto segment : segments)
  {
    // colorize the segments with random colors
    double r = static_cast<double>(rand()) / RAND_MAX;
    double g = static_cast<double>(rand()) / RAND_MAX;
    double b = static_cast<double>(rand()) / RAND_MAX;    
    for (int i = 0; i < segment->Points.size(); i++)
    {
      segment->Colors.push_back(Eigen::Vector3d(r, g, b));
    }
    vis.AddPointCloud(segment);
  }
  vis.Run();
  return 0;
}