#include "DFSegmentation.hh"

#include <cilantro/utilities/point_cloud.hpp>
#include <cilantro/core/nearest_neighbors.hpp>
#include <cilantro/clustering/connected_component_extraction.hpp>
#include <cmath>

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

    std::shared_ptr<geometry::DFPointCloud> DFSegmentation::AssociateClustersToMeshes(
        std::vector<std::shared_ptr<geometry::DFMesh>> referenceMesh,
        std::vector<std::shared_ptr<geometry::DFPointCloud>> &clusters,
        double angleThreshold,
        double associationThreshold)
    {
        std::shared_ptr<geometry::DFPointCloud> unifiedPointCloud = std::make_shared<geometry::DFPointCloud>();

        // iterate through the mesh faces given as function argument
        if (referenceMesh.size() == 0)
        {
            DIFFCHECK_WARN("No mesh faces to associate with the clusters. Returning an empty point cloud.");
            return unifiedPointCloud;
        }
        for (std::shared_ptr<diffCheck::geometry::DFMesh> face : referenceMesh)
        {
            std::shared_ptr<geometry::DFPointCloud> correspondingSegment;

            // Getting the center of the mesh face
            Eigen::Vector3d faceCenter = face->Cvt2O3DTriangleMesh()->GetCenter();

            // Getting the normal of the mesh face
            Eigen::Vector3d faceNormal = face->GetFirstNormal();
            faceNormal.normalize();
            
            double faceDistance = std::numeric_limits<double>::max();
            if (clusters.size() == 0)
            {
                DIFFCHECK_WARN("No clusters to associate with the mesh faces. Returning an empty point cloud.");
                return unifiedPointCloud;
            }
            for (auto segment : clusters)
            {   
                Eigen::Vector3d segmentCenter;
                Eigen::Vector3d segmentNormal;

                for (auto point : segment->Points){segmentCenter += point;}
                if (segment->GetNumPoints() > 0)
                {
                    segmentCenter /= segment->GetNumPoints();
                }
                else
                {
                    DIFFCHECK_WARN("Empty segment. Skipping the segment.");
                    continue;
                }

                for (auto normal : segment->Normals){segmentNormal += normal;}
                segmentNormal.normalize();

                double currentDistance = (faceCenter - segmentCenter).norm();
                // if the distance is smaller than the previous one, update the distance and the corresponding segment
                if (std::abs(sin(acos(faceNormal.dot(segmentNormal)))) < angleThreshold  && currentDistance < faceDistance)
                {
                    correspondingSegment = segment;
                    faceDistance = currentDistance;
                }
                
            }

            if (correspondingSegment == nullptr)
            {
                DIFFCHECK_WARN("No segment found for the face. Skipping the face.");
                continue;
            }
            for (Eigen::Vector3d point : correspondingSegment->Points)
            {
                bool pointInFace = false;
                if (face->IsPointOnFace(point, associationThreshold))
                {
                    unifiedPointCloud->Points.push_back(point);
                    unifiedPointCloud->Normals.push_back(
                        correspondingSegment->Normals[std::distance(
                            correspondingSegment->Points.begin(), 
                            std::find(correspondingSegment->Points.begin(), 
                            correspondingSegment->Points.end(), 
                            point))]
                        );
                }
            }
            // removing points from the segment that are in the face
            if (unifiedPointCloud->GetNumPoints() == 0)
            {
                DIFFCHECK_WARN("No point was associated to this segment. Skipping the segment.");
                continue;
            }
            for(Eigen::Vector3d point : unifiedPointCloud->Points)
            {
                correspondingSegment->Points.erase(
                    std::remove(
                        correspondingSegment->Points.begin(), 
                        correspondingSegment->Points.end(), 
                        point), 
                    correspondingSegment->Points.end());
            }
        }
        return unifiedPointCloud;
    }

    void DFSegmentation::CleanUnassociatedClusters(
        std::vector<std::shared_ptr<geometry::DFPointCloud>> &unassociatedClusters,
        std::vector<std::shared_ptr<geometry::DFPointCloud>> &existingPointCloudSegments,
        std::vector<std::vector<std::shared_ptr<geometry::DFMesh>>> meshes,
        double angleThreshold,
        double associationThreshold)
    {
        if (unassociatedClusters.size() == 0)
        {
            DIFFCHECK_WARN("No unassociated clusters. Nothing is done");
            return;
        }
        for (std::shared_ptr<geometry::DFPointCloud> cluster : unassociatedClusters)
        {
            std::shared_ptr<geometry::DFMesh> correspondingMeshFace;
            Eigen::Vector3d clusterCenter;
            Eigen::Vector3d clusterNormal = Eigen::Vector3d::Zero();

            if (cluster->GetNumPoints() == 0)
            {
                DIFFCHECK_WARN("Empty cluster. Skipping the cluster.");
                continue;
            }
            for (Eigen::Vector3d point : cluster->Points)
            {
                clusterCenter += point;
            }
            clusterCenter /= cluster->GetNumPoints();
            if (cluster->GetNumNormals() == 0)
            {
                DIFFCHECK_WARN("Empty normals in the cluster. Skipping the cluster.");
                continue;
            }
            for (Eigen::Vector3d normal : cluster->Normals)
            {
                clusterNormal += normal;
            }
            clusterNormal.normalize();

            int meshIndex = 0;
            int faceIndex = 0 ;
            int goodMeshIndex = 0;
            int goodFaceIndex = 0;
            double distance = std::numeric_limits<double>::max();

            if (meshes.size() == 0)
            {
                DIFFCHECK_WARN("No meshes to associate with the clusters. Skipping the cluster.");
                continue;
            }
            for (std::vector<std::shared_ptr<geometry::DFMesh>> mesh : meshes)
            {
                if (mesh.size() == 0)
                {
                    DIFFCHECK_WARN("Empty piece in the meshes vector. Skipping the mesh face vector.");
                    continue;
                }
                for (std::shared_ptr<geometry::DFMesh> meshFace : mesh)
                {
                    Eigen::Vector3d faceCenter = Eigen::Vector3d::Zero();
                    Eigen::Vector3d faceNormal = Eigen::Vector3d::Zero();
  
                    std::shared_ptr<open3d::geometry::TriangleMesh> o3dFace = meshFace->Cvt2O3DTriangleMesh();
                    
                    faceNormal = meshFace->GetFirstNormal();
                    faceNormal.normalize();
                    faceCenter = o3dFace->GetCenter();
                    /*
                    To make sure we select the right meshFace, we add another metric:
                    Indeed, from experimentation, sometimes the wrong mesh face is selected, because it is parallel to the correct one 
                    (so the normal don't play a role) and the center of the face is closer to the cluster center than the correct face.
                    To prevent this, we take into the account the angle between the line linking the center of the meshFace considered 
                    and the center of the point cloud cluster and the normal of the cluster. This value should be close to pi/2

                    The following two lines are not super optimized but more readable than the optimized version
                    */

                    double dotProduct = clusterNormal.dot((clusterCenter - faceCenter).normalized());
                    dotProduct = std::max(-1.0, std::min(1.0, dotProduct));
                    double clusterNormalToJunctionLineAngle = std::acos(dotProduct);
                    
                    double currentDistance = (clusterCenter - faceCenter).norm() * std::abs(std::cos(clusterNormalToJunctionLineAngle))
                    / std::min(std::abs(clusterNormal.dot(faceNormal)), 0.05) ;
                    if (std::abs(sin(acos(faceNormal.dot(clusterNormal)))) < angleThreshold && currentDistance < distance)
                    {
                        goodMeshIndex = meshIndex;
                        goodFaceIndex = faceIndex;
                        distance = currentDistance;
                        correspondingMeshFace = meshFace;
                    }
                    faceIndex++;
                }
                meshIndex++;
            }

            if (correspondingMeshFace == nullptr)
            {
                DIFFCHECK_WARN("No mesh face found for the cluster. Skipping the cluster.");
                continue;
            }
            if (goodMeshIndex >= existingPointCloudSegments.size())
            {
                DIFFCHECK_WARN("No segment found for the face. Skipping the face.");
                continue;
            }
            std::shared_ptr<geometry::DFPointCloud> completed_segment = existingPointCloudSegments[goodMeshIndex];

            for (Eigen::Vector3d point : cluster->Points)
            {
                if (correspondingMeshFace->IsPointOnFace(point, associationThreshold))
                {
                    completed_segment->Points.push_back(point);
                    completed_segment->Normals.push_back(cluster->Normals[std::distance(cluster->Points.begin(), std::find(cluster->Points.begin(), cluster->Points.end(), point))]);
                }
            }
            std::vector<int> indicesToRemove;

            for (int i = 0; i < cluster->Points.size(); ++i) 
            {
                if (std::find(completed_segment->Points.begin(), completed_segment->Points.end(), cluster->Points[i]) != completed_segment->Points.end()) 
                {
                    indicesToRemove.push_back(i);
                }
            }
            for (auto it = indicesToRemove.rbegin(); it != indicesToRemove.rend(); ++it) 
            {
                std::swap(cluster->Points[*it], cluster->Points.back());
                cluster->Points.pop_back();
                std::swap(cluster->Normals[*it], cluster->Normals.back());
                cluster->Normals.pop_back();
            }
        }
    };

} // namespace diffCheck::segmentation