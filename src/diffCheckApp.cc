#include "diffCheck.hh"
#include "diffCheck/log.hh"

#include <iostream>
#include <fstream>
#include <chrono>

int main()
{
  std::shared_ptr<diffCheck::geometry::DFPointCloud> pcdSrc = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::vector<std::shared_ptr<diffCheck::geometry::DFPointCloud>> segments;
  std::string pathPcdSrc = R"(C:\Users\andre\Downloads\moved_04.ply)";

  pcdSrc->LoadFromPLY(pathPcdSrc);

  pcdSrc->EstimateNormals();
  segments = diffCheck::segmentation::DFSegmentation::NormalBasedSegmentation(
    pcdSrc,
    20.f,
    10,
    true,
    50,
    0.5f,
    true);
  std::cout << "number of segments:" << segments.size()<< std::endl;

  std::tuple<std::shared_ptr<diffCheck::geometry::DFPointCloud>, std::vector<std::shared_ptr<diffCheck::geometry::DFPointCloud>>> unifiedSegments = 
    diffCheck::segmentation::DFSegmentation::AssociateSegments(meshSrc, segments, 0.15);

  diffCheck::visualizer::Visualizer vis;
  vis.AddMesh(meshSrc);
  for (auto segment : segments)
    vis->AddPointCloud(segment);

  }
  
  for(auto mesh : meshSrc)
  {
    vis.AddMesh(mesh);
  }

  auto unified = std::get<0>(unifiedSegments);
  for (int i = 0; i < unified->Points.size(); i++)
  {
    unified->Colors.push_back(Eigen::Vector3d(0, 0, 0));
  }
  vis.AddPointCloud(unified);

  auto endTime = std::chrono::high_resolution_clock::now();
  auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - initTime);
  std::cout << "Computation time:" << duration.count() << std::endl;

  vis.Run();
  return 0;
}