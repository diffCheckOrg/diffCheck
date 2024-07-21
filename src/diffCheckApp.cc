#include "diffCheck.hh"
#include "diffCheck/log.hh"
#include "diffCheck/IOManager.hh"

#include <filesystem>
#include <iostream>
#include <fstream>


// checking computation time 
#include <chrono>

int main()
{
  auto initTime = std::chrono::high_resolution_clock::now();

  std::shared_ptr<diffCheck::geometry::DFPointCloud> pcdSrc = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::string pathTest = diffCheck::io::GetRoofQuarterPlyPath();
  std::cout << "Path to the test file: " << pathTest << std::endl;
  
  pcdSrc->LoadFromPLY(diffCheck::io::GetRoofQuarterPlyPath());

  diffCheck::visualizer::Visualizer vis(std::string("DiffCheckApp"), 1000, 800, 50, 50, false, true, false);
  vis.AddPointCloud(pcdSrc);

  vis.Run();

  return 0;
}