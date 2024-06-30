#include "DFSegmentation.hh"

#include <cilantro/utilities/point_cloud.hpp>
#include <cilantro/core/nearest_neighbors.hpp>
#include <cilantro/clustering/connected_component_extraction.hpp>

namespace diffCheck::segmentation
{   
    std::vector<std::shared_ptr<geometry::DFPointCloud>> DFSegmentation::NormalBasedSegmentation(
        std::shared_ptr<geometry::DFPointCloud> &pointCloud,
        float normalThresholdDegree,
        int minClusterSize,
        bool useKnnNeighborhood,
        int knnNeighborhoodSize,
        int radiusNeighborhoodSize,
        bool colorClusters)
    {
        std::shared_ptr<cilantro::PointCloud3f> cilantroPointCloud = pointCloud->Cvt2CilantroPointCloud();

        std::vector<std::shared_ptr<geometry::DFPointCloud>> segments;
        if (useKnnNeighborhood)
        {
            cilantro::KNNNeighborhoodSpecification<int> neighborhood(knnNeighborhoodSize);

            // FIXME: not clear why this is needed all the time
            cilantroPointCloud->estimateNormals(neighborhood);

            cilantro::NormalsProximityEvaluator<float, 3> similarityEvaluator(
            cilantroPointCloud->normals, 
            normalThresholdDegree*M_PI/180.0f);

            cilantro::ConnectedComponentExtraction3f<> segmenter(cilantroPointCloud->points);
            segmenter.segment(neighborhood, similarityEvaluator, minClusterSize);
            auto clusterToPointMap = segmenter.getClusterToPointIndicesMap();
            int nSegments = segmenter.getNumberOfClusters();

            for (int indice = 0; indice<nSegments; indice++)
            {
                std::shared_ptr<geometry::DFPointCloud> segment = std::make_shared<geometry::DFPointCloud>();
                for (auto pointIndice : clusterToPointMap[indice])
                {
                    Eigen::Vector3d point = cilantroPointCloud->points.col(pointIndice).cast<double>();
                    Eigen::Vector3d normal = cilantroPointCloud->normals.col(pointIndice).cast<double>();
                    segment->Points.push_back(point);
                    segment->Normals.push_back(normal);
                    if (cilantroPointCloud->hasColors())
                    {
                        Eigen::Vector3d color = cilantroPointCloud->colors.col(pointIndice).cast<double>();
                        segment->Colors.push_back(color);
                    }
                }
                if (colorClusters)
                    segment->ApplyColor(Eigen::Vector3d::Random());
                segments.push_back(segment);
            }
        }
        else
        {
            cilantro::RadiusNeighborhoodSpecification<float> neighborhood(radiusNeighborhoodSize);

            // cilantroPointCloud->estimateNormals(neighborhood);

            cilantro::NormalsProximityEvaluator<float, 3> similarityEvaluator(
            cilantroPointCloud->normals,
            normalThresholdDegree*M_PI/180.0f);

            cilantro::ConnectedComponentExtraction3f<> segmenter(cilantroPointCloud->points);
            segmenter.segment(neighborhood, similarityEvaluator, minClusterSize);

            auto clusterToPointMap = segmenter.getClusterToPointIndicesMap();
            int nSegments = segmenter.getNumberOfClusters();

            for (int indice = 0; indice<nSegments; indice++)
            {
                std::shared_ptr<geometry::DFPointCloud> segment = std::make_shared<geometry::DFPointCloud>();
                for (auto pointIndice : clusterToPointMap[indice])
                {
                    Eigen::Vector3d point = cilantroPointCloud->points.col(pointIndice).cast<double>();
                    Eigen::Vector3d normal = cilantroPointCloud->normals.col(pointIndice).cast<double>();
                    segment->Points.push_back(point);
                    segment->Normals.push_back(normal);
                }
                segments.push_back(segment);
            }
        }

        return segments;
    }
} // namespace diffCheck::segmentation