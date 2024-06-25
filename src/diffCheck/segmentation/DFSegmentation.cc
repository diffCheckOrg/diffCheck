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

    std::tuple<std::shared_ptr<geometry::DFPointCloud>, std::vector<std::shared_ptr<geometry::DFPointCloud>>> DFSegmentation::AssociateSegments(
        std::vector<std::shared_ptr<geometry::DFMesh>> meshFaces,
        std::vector<std::shared_ptr<geometry::DFPointCloud>> segments,
        double associationThreshold)
    {
        std::shared_ptr<geometry::DFPointCloud> unifiedPointCloud = std::make_shared<geometry::DFPointCloud>();
        std::vector<std::shared_ptr<geometry::DFPointCloud>> segmentsRemainder;

        // iterate through the mesh faces given as function argument
        for (auto face : meshFaces)
        {
            std::shared_ptr<geometry::DFPointCloud> correspondingSegment;
            
            // Getting the center of the mesh face
            Eigen::Vector3d faceCenter = Eigen::Vector3d::Zero();
            for (auto vertex : face->Vertices){faceCenter += vertex;}
            faceCenter /= face->GetNumVertices();

            if (face->NormalsFace.size() == 0)
            {
                std::cout << "face has no normals, computing normals" << std::endl;
                std::shared_ptr<open3d::geometry::TriangleMesh> o3dFace = face->Cvt2O3DTriangleMesh();
                o3dFace->ComputeTriangleNormals();
                face->NormalsFace.clear();
                for (auto normal : o3dFace->triangle_normals_)
                {
                    face->NormalsFace.push_back(normal.cast<double>());
                }
            }

            // Getting the normal of the mesh face
            Eigen::Vector3d faceNormal = face->NormalsFace[0];

            // iterate through the segments to find the closest ones compared to the face center taking the normals into account
            Eigen::Vector3d segmentCenter = Eigen::Vector3d::Zero();
            Eigen::Vector3d segmentNormal = Eigen::Vector3d::Zero();
            double faceDistance = (segments[0]->Points[0] - faceCenter).norm() / std::pow(std::abs(segments[0]->Normals[0].dot(faceNormal)), 2);
            int segmentIndex = 0;
            for (auto segment : segments)
            {
                for (auto point : segment->Points)
                {
                    segmentCenter += point;
                }
                segmentCenter /= segment->GetNumPoints();

                if (segment->Normals.size() == 0)
                {
                    std::shared_ptr<open3d::geometry::PointCloud> o3dSegment = segment->Cvt2O3DPointCloud();
                    o3dSegment->EstimateNormals();
                    segment->Normals.clear();
                    for (auto normal : o3dSegment->normals_)
                    {
                        segment->Normals.push_back(normal.cast<double>());
                    }
                }
                for (auto normal : segment->Normals)
                {
                    segmentNormal += normal;
                }
                segmentNormal.normalize();

                double currentDistance = (faceCenter - segmentCenter).norm() / std::pow(std::abs(segmentNormal.dot(faceNormal)), 2);
                // if the distance is smaller than the previous one, update the distance and the corresponding segment
                if (currentDistance < faceDistance)
                {
                    correspondingSegment = segment;
                    // storing previous segment in the remainder vector
                    faceDistance = currentDistance;
                }
                segmentIndex++;
            }
            // remove the segment fron the segments vector
            segments.erase(std::remove(segments.begin(), segments.end(), correspondingSegment), segments.end());
            
            // Add the closest points of the corresponding segment to the unified point cloud
            for (auto point : correspondingSegment->Points)
            {
                unifiedPointCloud->Points.push_back(point);
                correspondingSegment->Points.erase(std::remove(correspondingSegment->Points.begin(), correspondingSegment->Points.end(), point), correspondingSegment->Points.end());
            }
        }
        return std::make_tuple(unifiedPointCloud, segments);
    }

} // namespace diffCheck::segmentation