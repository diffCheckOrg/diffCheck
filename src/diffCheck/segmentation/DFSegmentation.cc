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
        float radiusNeighborhoodSize,
        bool colorClusters)
    {
        if (!pointCloud->HasNormals())
        {
            DIFFCHECK_WARN("The point cloud does not have normals. Estimating normals with 50 neighbors.");
            pointCloud->EstimateNormals(true, 50);
        }

        std::shared_ptr<cilantro::PointCloud3f> cilantroPointCloud = pointCloud->Cvt2CilantroPointCloud();

        std::vector<std::shared_ptr<geometry::DFPointCloud>> segments;
        if (useKnnNeighborhood)
        {
            cilantro::KNNNeighborhoodSpecification<int> neighborhood(knnNeighborhoodSize);

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
        for (std::shared_ptr<diffCheck::geometry::DFMesh> face : meshFaces)
        {
            std::shared_ptr<geometry::DFPointCloud> correspondingSegment;
            std::shared_ptr<open3d::geometry::TriangleMesh> o3dFace;
            o3dFace = face->Cvt2O3DTriangleMesh();

            // Getting the center of the mesh face
            Eigen::Vector3d faceCenter;
            open3d::geometry::OrientedBoundingBox orientedBoundingBox = o3dFace->GetMinimalOrientedBoundingBox();
            faceCenter = orientedBoundingBox.GetCenter();

            if (face->NormalsFace.size() == 0)
            {
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
            Eigen::Vector3d segmentCenter;
            Eigen::Vector3d segmentNormal;
            double faceDistance = std::numeric_limits<double>::max();
            for (auto segment : segments)
            {
                for (auto point : segment->Points)
                {
                    segmentCenter += point;
                }
                segmentCenter /= segment->GetNumPoints();

                for (auto normal : segment->Normals)
                {
                    segmentNormal += normal;
                }
                segmentNormal.normalize();

                double currentDistance = (faceCenter - segmentCenter).norm() / std::abs(segmentNormal.dot(faceNormal));
                // if the distance is smaller than the previous one, update the distance and the corresponding segment
                if (currentDistance < faceDistance)
                {
                    correspondingSegment = segment;
                    faceDistance = currentDistance;
                }
            }
            
            // get the triangles of the face. This is to check if the point is in the face
            std::vector<Eigen::Vector3i> faceTriangles = o3dFace->triangles_;

            for (Eigen::Vector3d point : correspondingSegment->Points)
            {
                bool pointInFace = false;
                /*
                To check if the point is in the face, we take into account all the triangles forming the face.
                We calculate the area of each triangle, then check if the sum of the areas of the tree triangles 
                formed by two of the points of the referencr triangle and our point is equal to the reference triangle area 
                (within a user-defined margin). If it is the case, the triangle is in the face.
                */
                for (Eigen::Vector3i triangle : faceTriangles)
                {
                    // reference triangle
                    Eigen::Vector3d v0 = o3dFace->vertices_[triangle[0]];
                    Eigen::Vector3d v1 = o3dFace->vertices_[triangle[1]];
                    Eigen::Vector3d v2 = o3dFace->vertices_[triangle[2]];
                    Eigen::Vector3d n = (v1 - v0).cross(v2 - v0);
                    double referenceTriangleArea = n.norm()*0.5;
                    
                    // triangle 1
                    Eigen::Vector3d n1 = (v1 - v0).cross(point - v0);
                    double area1 = n1.norm()*0.5;

                    // triangle 2
                    Eigen::Vector3d n2 = (v2 - v1).cross(point - v1);
                    double area2 = n2.norm()*0.5;

                    // triangle 3
                    Eigen::Vector3d n3 = (v0 - v2).cross(point - v2);
                    double area3 = n3.norm()*0.5;

                    double res = ( area1 + area2 + area3 - referenceTriangleArea) / referenceTriangleArea;
                    if (res < associationThreshold)
                    {
                        pointInFace = true;
                        break;
                    }
                }
                if (pointInFace)
                {
                    unifiedPointCloud->Points.push_back(point);
                }
            }
            // removing points from the segment that are in the face
            for(Eigen::Vector3d point : unifiedPointCloud->Points)
            {
                correspondingSegment->Points.erase(std::remove(correspondingSegment->Points.begin(), correspondingSegment->Points.end(), point), correspondingSegment->Points.end());
            }
        }
        return std::make_tuple(unifiedPointCloud, segments);
    }

} // namespace diffCheck::segmentation