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

  std::vector<std::vector<std::shared_ptr<diffCheck::geometry::DFMesh>>> meshSrc = std::vector<std::vector<std::shared_ptr<diffCheck::geometry::DFMesh>>>();
  std::vector<std::shared_ptr<diffCheck::geometry::DFPointCloud>> segments;
  std::vector<std::string> meshPaths;

  std::string meshesFolderPath = R"(C:\Users\localuser\Desktop\meshes_for_diffCheck\joints\)";

  for (int i = 1; i <= 3; i++)
  {
    std::vector<std::shared_ptr<diffCheck::geometry::DFMesh>> fullJoint;
    for (int j = 1; j <= 3; j++)
    {
      std::string meshPath = meshesFolderPath + std::to_string(i) + "/" + std::to_string(j) + ".ply";
      std::shared_ptr<diffCheck::geometry::DFMesh> mesh = std::make_shared<diffCheck::geometry::DFMesh>();
      mesh->LoadFromPLY(meshPath);
      fullJoint.push_back(mesh);
    }
    meshSrc.push_back(fullJoint);
  }

  std::string pathPcdSrc = R"(C:\Users\localuser\Desktop\meshes_for_diffCheck\joints\full_beam.ply)";

  pcdSrc->LoadFromPLY(pathPcdSrc);

  pcdSrc->EstimateNormals(false, 100);
  pcdSrc->VoxelDownsample(0.007);
  auto intermediateTime = std::chrono::high_resolution_clock::now();
  segments = diffCheck::segmentation::DFSegmentation::NormalBasedSegmentation(
    pcdSrc,
    15.0f,
    15,
    true,
    50,
    0.5f,
    false);
  std::cout << "number of segments:" << segments.size()<< std::endl;

  std::vector<std::shared_ptr<diffCheck::geometry::DFPointCloud>> unifiedSegments;
  for (int i = 0; i < meshSrc.size(); i++)
  {
    std::shared_ptr<diffCheck::geometry::DFPointCloud> unifiedSegment = std::make_shared<diffCheck::geometry::DFPointCloud>();
    unifiedSegment = diffCheck::segmentation::DFSegmentation::AssociateClustersToMeshes(
      meshSrc[i], 
      segments, 
      .2, 
      .05);
    unifiedSegments.push_back(unifiedSegment);
  }

  diffCheck::segmentation::DFSegmentation::CleanUnassociatedClusters(segments, 
    unifiedSegments, 
    meshSrc,
    .2, 
    .05);

  // Perform a registration per joint
  for (int i = 0; i < meshSrc.size(); i++)
  {
    std::shared_ptr<diffCheck::geometry::DFPointCloud> referencePointCloud = std::make_shared<diffCheck::geometry::DFPointCloud>();
    for (auto jointFace : meshSrc[i])
    {
      std::shared_ptr<diffCheck::geometry::DFPointCloud> facePointCloud = jointFace->SampleCloudUniform(1000);
      referencePointCloud->Points.insert(referencePointCloud->Points.end(), facePointCloud->Points.begin(), facePointCloud->Points.end());
    }
    referencePointCloud->EstimateNormals(false, 100);

    diffCheck::transformation::DFTransformation transformation = diffCheck::registrations::DFRefinedRegistration::O3DICP(
      unifiedSegments[i],
      referencePointCloud);

    std::cout << "Transformation matrix:" << std::endl;
    std::cout << transformation.TransformationMatrix << std::endl;

    diffCheck::visualizer::Visualizer deVisu = diffCheck::visualizer::Visualizer("DiffCheckApp", 1000, 800, 50, 50, false, true, false);
    for (int i = 0; i < segments.size(); i++)
    {
      segments[i]->ApplyTransformation(transformation);
      deVisu.AddPointCloud(segments[i]);
    }
    for (auto joint : meshSrc)
    {
      for (auto face : joint)
      {
        deVisu.AddMesh(face);
      }
    }
    deVisu.Run();
  }
    
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
  for(auto joint : meshSrc)
  {
    for(auto mesh : joint){vis.AddMesh(mesh);}
  }

  int numSegments = unifiedSegments.size();

  for (int i = 0; i < numSegments; i++)
  {
    for (int j = 0; j < unifiedSegments[i]->Points.size(); j++)
    {
      unifiedSegments[i]->Colors.push_back(Eigen::Vector3d((double(numSegments) - double(i))/double(numSegments), 1, double(i) / double(numSegments)));
    }
  }
  for (auto seg : unifiedSegments)
  {
    vis.AddPointCloud(seg);
  }

  auto endTime = std::chrono::high_resolution_clock::now();
  auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - initTime);
  auto segmentationTime = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - intermediateTime);
  std::cout << "Total computation time:" << duration.count() << std::endl;
  std::cout << "Segmentation time:" << segmentationTime.count() << std::endl;

  vis.Run();

  return 0;
}