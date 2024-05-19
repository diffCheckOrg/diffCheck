#include "diffCheck.hh"

#include <iostream>
#include <fstream>


int main()
{
  std::shared_ptr<diffCheck::geometry::DFPointCloud> pcdSrc = std::make_shared<diffCheck::geometry::DFPointCloud>();

  std::string pathPcdSrc = R"(C:\Users\andre\Downloads\04_pt.ply)";

  pcdSrc->LoadFromPLY(pathPcdSrc);

  pcdSrc->DownsampleBySize(100);

  std::shared_ptr<diffCheck::visualizer::Visualizer> vis = std::make_shared<diffCheck::visualizer::Visualizer>();
  vis->AddPointCloud(pcdSrc);
  vis->Run();
  return 0;
}