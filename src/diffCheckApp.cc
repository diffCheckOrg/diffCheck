#include "diffCheck.hh"

#include <iostream>
#include <fstream>


int main()
{
  std::shared_ptr<diffCheck::geometry::DFPointCloud> pcdSrc = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFMesh> meshSrc = std::make_shared<diffCheck::geometry::DFMesh>();
  std::vector<std::shared_ptr<diffCheck::geometry::DFPointCloud>> segments;
  std::string pathMeshSrc = R"(C:\Users\localuser\Downloads\02_mesh.ply)";
  std::string pathPcdSrc = R"(C:\Users\localuser\Downloads\02_points_with_errors_1e6_pts.ply)";

  pcdSrc->LoadFromPLY(pathPcdSrc);
  meshSrc->LoadFromPLY(pathMeshSrc);

  segments = diffCheck::segmentation::DFSegmentation::NormalBasedSegmentation(*pcdSrc, 0.01, 1, 30, true, 50, 30);
  std::cout << "number of segments:" << segments.size()<< std::endl;

  diffCheck::visualizer::Visualizer vis;
  vis.AddMesh(meshSrc);
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