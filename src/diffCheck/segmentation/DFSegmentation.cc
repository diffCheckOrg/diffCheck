#include "DFSegmentation.hh"

#include <cilantro/utilities/point_cloud.hpp>
#include <cilantro/core/nearest_neighbors.hpp>
#include <cilantro/clustering/connected_component_extraction.hpp>

namespace diffCheck::segmentation
{   
    std::vector<std::shared_ptr<geometry::DFPointCloud>> DFSegmentation::NormalBasedSegmentation(
        geometry::DFPointCloud &pointCloud,
        float voxelSize,
        float normalThresholdDegree,
        int minClusterSize,
        bool useKnnNeighborhood,
        int knnNeighborhoodSize,
        int radiusNeighborhoodSize)
    {
        std::vector<std::shared_ptr<geometry::DFPointCloud>> segments;
        cilantro::PointCloud3f cilantroPointCloud;
        
        // Convert the point cloud to cilantro point cloud
        for (int i = 0; i < pointCloud.Points.size();  i++)
        {
            cilantroPointCloud.points.conservativeResize(3, cilantroPointCloud.points.cols() + 1);
            cilantroPointCloud.points.rightCols(1) = pointCloud.Points[i].cast<float>();
        }

        // segment the point cloud using knn or radius neighborhood
        if (useKnnNeighborhood)
        {
            cilantro::KNNNeighborhoodSpecification<int> neighborhood(knnNeighborhoodSize);

            // conpute the normals and downsample
            cilantroPointCloud.estimateNormals(neighborhood, false);
            cilantroPointCloud.gridDownsample(voxelSize);

            // Similarity evaluator
            cilantro::NormalsProximityEvaluator<float, 3> similarityEvaluator(
            cilantroPointCloud.normals, 
            normalThresholdDegree*M_PI/180.0f);

            // Segment the point cloud
            cilantro::ConnectedComponentExtraction3f<> segmenter(cilantroPointCloud.points);
            segmenter.segment(neighborhood, similarityEvaluator, minClusterSize);
            auto clusterToPointMap = segmenter.getClusterToPointIndicesMap();
            int nSegments = segmenter.getNumberOfClusters();

            // Get the segments
            for (int indice = 0; indice<nSegments; indice++)
            {
                std::shared_ptr<geometry::DFPointCloud> segment = std::make_shared<geometry::DFPointCloud>();
                for (auto pointIndice : clusterToPointMap[indice])
                {
                    Eigen::Vector3d point = cilantroPointCloud.points.col(pointIndice).cast<double>();
                    Eigen::Vector3d normal = cilantroPointCloud.normals.col(pointIndice).cast<double>();
                    segment->Points.push_back(point);
                    segment->Normals.push_back(normal);
                }
                segments.push_back(segment);
            }
        }
        else
        {
            cilantro::RadiusNeighborhoodSpecification<float> neighborhood(radiusNeighborhoodSize);

            // conpute the normals and downsample
            cilantroPointCloud.estimateNormals(neighborhood, false);
            cilantroPointCloud.gridDownsample(voxelSize);
            
            // Similarity evaluator
            cilantro::NormalsProximityEvaluator<float, 3> similarityEvaluator(
            cilantroPointCloud.normals, 
            normalThresholdDegree*M_PI/180.0f);

            // Segment the point cloud
            cilantro::ConnectedComponentExtraction3f<> segmenter(cilantroPointCloud.points);
            segmenter.segment(neighborhood, similarityEvaluator, minClusterSize);

            auto clusterToPointMap = segmenter.getClusterToPointIndicesMap();
            int nSegments = segmenter.getNumberOfClusters();

            // Get the segments
            for (int indice = 0; indice<nSegments; indice++)
            {
                std::shared_ptr<geometry::DFPointCloud> segment = std::make_shared<geometry::DFPointCloud>();
                for (auto pointIndice : clusterToPointMap[indice])
                {
                    Eigen::Vector3d point = cilantroPointCloud.points.col(pointIndice).cast<double>();
                    Eigen::Vector3d normal = cilantroPointCloud.normals.col(pointIndice).cast<double>();
                    segment->Points.push_back(point);
                    segment->Normals.push_back(normal);
                }
                segments.push_back(segment);
            }
        }
        

        return segments;
    }
} // namespace diffCheck::segmentation