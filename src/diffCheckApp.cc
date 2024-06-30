#include "diffCheck.hh"
#include "diffCheck/log.hh"

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

  pcdSrc->EstimateNormals(100);
  segments = diffCheck::segmentation::DFSegmentation::NormalBasedSegmentation(
    pcdSrc,
    20.f,
    10,
    true,
    50,
    10,
    true);
  std::cout << "number of segments:" << segments.size()<< std::endl;

  std::shared_ptr<diffCheck::visualizer::Visualizer> vis = std::make_shared<diffCheck::visualizer::Visualizer>();
  vis->RenderPcdColorNormals = false;
  
  for (auto segment : segments)
    vis->AddPointCloud(segment);

  vis->Run();
  return 0;
}