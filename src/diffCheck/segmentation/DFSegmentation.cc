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
        open3d::geometry::PointCloud o3dPointCloud;
        cilantro::PointCloud3f cilantroPointCloud;

        // Convert the point cloud to open3d point cloud
        for (int i = 0; i < pointCloud.Points.size(); i++)
        {
            o3dPointCloud.points_.push_back(pointCloud.Points[i]);
        }

        // estimate normals
        o3dPointCloud.EstimateNormals(open3d::geometry::KDTreeSearchParamHybrid(50 * voxelSize, 80));
        o3dPointCloud.NormalizeNormals();
        std::shared_ptr<open3d::geometry::PointCloud> voxelizedO3DPointCloud = o3dPointCloud.VoxelDownSample(voxelSize);

        // Convert the point cloud to cilantro point cloud
        for (int i = 0; i < voxelizedO3DPointCloud->points_.size();  i++)
        {
            cilantroPointCloud.points.conservativeResize(3, cilantroPointCloud.points.cols() + 1);
            cilantroPointCloud.points.rightCols(1) = voxelizedO3DPointCloud->points_[i].cast<float>();
            cilantroPointCloud.normals.conservativeResize(3, cilantroPointCloud.normals.cols() + 1);
            cilantroPointCloud.normals.rightCols(1) = voxelizedO3DPointCloud->normals_[i].cast<float>();
        }

        // segment the point cloud using knn or radius neighborhood
        if (useKnnNeighborhood)
        {
            cilantro::KNNNeighborhoodSpecification<int> neighborhood(knnNeighborhoodSize);

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
                    Eigen::Vector3d v0 = o3dFace->vertices_[triangle[0]].cast<double>();
                    Eigen::Vector3d v1 = o3dFace->vertices_[triangle[1]].cast<double>();
                    Eigen::Vector3d v2 = o3dFace->vertices_[triangle[2]].cast<double>();
                    Eigen::Vector3d n = (v1 - v0).cross(v2 - v0);
                    double referenceTriangleArea = n.norm()/2.0;
                    
                    // triangle 1
                    Eigen::Vector3d n1 = (v1 - v0).cross(point - v0);
                    double area1 = n1.norm()/2.0;

                    // triangle 2
                    Eigen::Vector3d n2 = (v2 - v1).cross(point - v1);
                    double area2 = n2.norm()/2.0;

                    // triangle 3
                    Eigen::Vector3d n3 = (v0 - v2).cross(point - v2);
                    double area3 = n3.norm()/2.0;

                    if (std::abs((referenceTriangleArea - (area1 + area2 + area3)) / referenceTriangleArea) < associationThreshold)
                    {
                        pointInFace = true;
                        break;
                    }
                }
                if (pointInFace)
                {
                    unifiedPointCloud->Points.push_back(point);
                    correspondingSegment->Points.erase(std::remove(correspondingSegment->Points.begin(), correspondingSegment->Points.end(), point), correspondingSegment->Points.end());
                }
                // correspondingSegment->Points.erase(std::remove(correspondingSegment->Points.begin(), correspondingSegment->Points.end(), point), correspondingSegment->Points.end());
            }
        }
        return std::make_tuple(unifiedPointCloud, segments);
    }

} // namespace diffCheck::segmentation