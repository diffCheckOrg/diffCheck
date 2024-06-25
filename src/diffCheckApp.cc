#include "diffCheck.hh"

#include <iostream>
#include <fstream>


int main()
{
  std::shared_ptr<diffCheck::geometry::DFPointCloud> pcdSrc = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::vector<std::shared_ptr<diffCheck::geometry::DFMesh>> meshSrc = std::vector<std::shared_ptr<diffCheck::geometry::DFMesh>>();
  std::vector<std::shared_ptr<diffCheck::geometry::DFPointCloud>> segments;
  std::vector<std::string> meshPaths;

  std::string meshesFolderPath = R"(C:\Users\localuser\Desktop\other_meshes_for_diffCheck\)";

  for (int i = 1; i <= 14; i++)
  {
    std::string meshPath = meshesFolderPath + std::to_string(i) + ".ply";
    std::shared_ptr<diffCheck::geometry::DFMesh> mesh = std::make_shared<diffCheck::geometry::DFMesh>();
    mesh->LoadFromPLY(meshPath);
    meshSrc.push_back(mesh);
  }

  std::string pathPcdSrc = R"(C:\Users\localuser\Downloads\02_points_with_errors_1e6_pts.ply)";

  pcdSrc->LoadFromPLY(pathPcdSrc);

  segments = diffCheck::segmentation::DFSegmentation::NormalBasedSegmentation(*pcdSrc, 5, 1, 20, true, 50, 200);
  std::cout << "number of segments:" << segments.size()<< std::endl;

  std::tuple<std::shared_ptr<diffCheck::geometry::DFPointCloud>, std::vector<std::shared_ptr<diffCheck::geometry::DFPointCloud>>> unifiedSegments = 
    diffCheck::segmentation::DFSegmentation::AssociateSegments(meshSrc, segments, 50);
  

  diffCheck::visualizer::Visualizer vis;
  for (int i = 0; i < 1; i++)
  {
    // colorize the segments with random colors
    double r = static_cast<double>(rand()) / RAND_MAX;
    double g = static_cast<double>(rand()) / RAND_MAX;
    double b = static_cast<double>(rand()) / RAND_MAX;    
    for (int i = 0; i < std::get<0>(unifiedSegments)->Points.size(); i++)
    {
      std::get<0>(unifiedSegments)->Colors.push_back(Eigen::Vector3d(r, g, b));
    }
    vis.AddPointCloud(std::get<0>(unifiedSegments));

    for (auto segemt : std::get<1>(unifiedSegments))
    {
      for (int i = 0; i < segemt->Points.size(); i++)
      {
        segemt->Colors.push_back(Eigen::Vector3d(0, 0, 1));
      }
      vis.AddPointCloud(segemt);
    }

  }
  vis.Run();
  return 0;
}