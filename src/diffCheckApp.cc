#include "diffCheck.hh"

#include <iostream>
#include <fstream>


int main()
{
  // import clouds
  std::shared_ptr<diffCheck::geometry::DFPointCloud> pcdSrc = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> pcdTgt = std::make_shared<diffCheck::geometry::DFPointCloud>();

  std::string pathPcdSrc = R"(C:\Users\andre\Downloads\04_pt.ply)";
  std::string pathPcdTgt = R"(C:\Users\andre\Downloads\moved_04.ply)";

  pcdSrc->LoadFromPLY(pathPcdSrc);
  pcdTgt->LoadFromPLY(pathPcdTgt);

  // global registration
  diffCheck::transformation::DFTransformation xform = 
    diffCheck::registrations::DFGlobalRegistrations::O3DFastGlobalRegistrationFeatureMatching(
        pcdSrc, pcdTgt);

  pcdTgt->ApplyTransformation(xform);



  std::shared_ptr<diffCheck::visualizer::Visualizer> vis = std::make_shared<diffCheck::visualizer::Visualizer>();
  vis->AddPointCloud(pcdSrc);
  vis->AddPointCloud(pcdTgt);
  vis->Run();
  return 0;
}