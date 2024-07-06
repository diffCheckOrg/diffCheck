#include "diffCheck.hh"
#include "diffCheck/log.hh"

#include <iostream>
#include <fstream>

// checking computation time 
#include <chrono>

int main()
{
  auto initTime = std::chrono::high_resolution_clock::now();

  std::shared_ptr<diffCheck::geometry::DFPointCloud> pcdSrc = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::vector<std::shared_ptr<diffCheck::geometry::DFMesh>> meshSrc = std::vector<std::shared_ptr<diffCheck::geometry::DFMesh>>();
  std::vector<std::shared_ptr<diffCheck::geometry::DFPointCloud>> segments;
  std::vector<std::string> meshPaths;

  std::string meshesFolderPath = R"(C:\Users\localuser\Desktop\again_other_meshes_for_diffCheck\6\)";

  for (int i = 1; i <= 4; i++)
  {
    std::string meshPath = meshesFolderPath + std::to_string(i) + ".ply";
    std::shared_ptr<diffCheck::geometry::DFMesh> mesh = std::make_shared<diffCheck::geometry::DFMesh>();
    mesh->LoadFromPLY(meshPath);
    meshSrc.push_back(mesh);
  }

  std::string pathPcdSrc = R"(C:\Users\localuser\Desktop\again_other_meshes_for_diffCheck\source_pc.ply)";

  pcdSrc->LoadFromPLY(pathPcdSrc);

  pcdSrc->EstimateNormals(false, 40);
  auto intermediateTime = std::chrono::high_resolution_clock::now();
  segments = diffCheck::segmentation::DFSegmentation::NormalBasedSegmentation(
    pcdSrc,
    2.0f,
    200,
    true,
    100,
    0.5f,
    false);
  std::cout << "number of segments:" << segments.size()<< std::endl;

  std::shared_ptr<diffCheck::geometry::DFPointCloud> unifiedSegments = 
    diffCheck::segmentation::DFSegmentation::AssociateClustersToMeshes(meshSrc, segments, .15);
  
  diffCheck::segmentation::DFSegmentation::CleanUnassociatedClusters(segments, std::vector<std::shared_ptr<diffCheck::geometry::DFPointCloud>>{unifiedSegments}, std::vector<std::vector<std::shared_ptr<diffCheck::geometry::DFMesh>>>{meshSrc}, .15);
  
  std::cout << "number of points in unified segments:" << unifiedSegments->Points.size() << std::endl;
  
  diffCheck::visualizer::Visualizer vis(std::string("DiffCheckApp"), 1000, 800, 50, 50, false, true, false);
  for (auto segment : segments)
  {
    // colorize the segments with random colors
    double r = static_cast<double>(rand()) / RAND_MAX;
    double g = static_cast<double>(rand()) / RAND_MAX;
    double b = static_cast<double>(rand()) / RAND_MAX;

    segment->Colors.clear();
    for (int i = 0; i < segment->Points.size(); i++)
    {
      segment->Colors.push_back(Eigen::Vector3d(0, 0, 0));
    }
  vis.AddPointCloud(segment);

  }
  for(auto mesh : meshSrc)
  {
    vis.AddMesh(mesh);
  }

  for (int i = 0; i < unifiedSegments->Points.size(); i++)
  {
    unifiedSegments->Colors.push_back(Eigen::Vector3d(0, 0, 1));
  }
  vis.AddPointCloud(unifiedSegments);

  auto endTime = std::chrono::high_resolution_clock::now();
  auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - initTime);
  auto segmentationTime = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - intermediateTime);
  std::cout << "Total computation time:" << duration.count() << std::endl;
  std::cout << "Segmentation time:" << segmentationTime.count() << std::endl;

  vis.Run();


  return 0;
}