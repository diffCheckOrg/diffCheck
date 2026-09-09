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

    std::vector<std::shared_ptr<geometry::DFPointCloud>> DFSegmentation::AssociateClustersToMeshes(
        bool isCylinder,
        bool discriminatePoints,
        std::vector<std::shared_ptr<geometry::DFMesh>> referenceMesh,
        std::vector<std::shared_ptr<geometry::DFPointCloud>> &clusters,
        double angleThreshold,
        double associationThreshold,
        double maximumFaceSegmentDistance)
    {
        std::vector<std::shared_ptr<geometry::DFPointCloud>> faceSegments = std::vector<std::shared_ptr<geometry::DFPointCloud>>();

        // iterate through the mesh faces given as function argument
        if (referenceMesh.size() == 0)
        {
            DIFFCHECK_WARN("No mesh faces to associate with the clusters. Returning an empty point cloud.");
            return std::vector<std::shared_ptr<geometry::DFPointCloud>>();
        }

        //differentiate between cylinder and other shapes
        if (isCylinder)
        {
            for (std::shared_ptr<diffCheck::geometry::DFMesh> face : referenceMesh)
            {
                std::tuple<Eigen::Vector3d, Eigen::Vector3d> centerAndAxis = face->ComputeOBBCenterAndAxis();
                Eigen::Vector3d cylinderCenter = std::get<0>(centerAndAxis);
                Eigen::Vector3d cylinderAxis = std::get<1>(centerAndAxis);

                double faceDistance = std::numeric_limits<double>::max();
                std::shared_ptr<geometry::DFPointCloud> correspondingSegment;
                std::shared_ptr<geometry::DFPointCloud> facePoints = std::make_shared<geometry::DFPointCloud>();

                Eigen::Vector3d min = face->Vertices[0];
                Eigen::Vector3d max = face->Vertices[0];
                for (auto vertex : face->Vertices)
                {
                    if(vertex.x() < min.x()){min.x() = vertex.x();}
                    if(vertex.y() < min.y()){min.y() = vertex.y();}
                    if(vertex.z() < min.z()){min.z() = vertex.z();}
                    if(vertex.x() > max.x()){max.x() = vertex.x();}
                    if(vertex.y() > max.y()){max.y() = vertex.y();}
                    if(vertex.z() > max.z()){max.z() = vertex.z();}
                    
                }

                if (clusters.size() == 0)
                {
                    DIFFCHECK_WARN("No clusters to associate with the mesh faces. Returning an empty point cloud.");
                    return std::vector<std::shared_ptr<geometry::DFPointCloud>>();
                }
                for (auto segment : clusters)
                {
                    Eigen::Vector3d segmentCenter;
                    Eigen::Vector3d segmentNormal;

                    for (auto point : segment->Points)
                    {
                        segmentCenter += point;
                    }
                    if (segment->GetNumPoints() > 0)
                    {
                        segmentCenter /= segment->GetNumPoints();
                    }
                    else
                    {
                        DIFFCHECK_WARN("Empty segment. Skipping the segment.");
                        continue;
                    }

                    for (auto normal : segment->Normals)
                    {
                        segmentNormal += normal;
                    }
                    segmentNormal.normalize();

                    // we consider the distance to the cylinder axis, not the cylinder center
                    Eigen::Vector3d projectedSegmentCenter = (segmentCenter - cylinderCenter).dot(cylinderAxis) * cylinderAxis + cylinderCenter;
                    double currentDistance = (cylinderCenter - projectedSegmentCenter).norm();
                    double absoluteDistance = (segmentCenter - cylinderCenter).norm();
                    if (std::abs(cylinderAxis.dot(segmentNormal)) < angleThreshold && currentDistance < faceDistance && absoluteDistance < (max - min).norm()*associationThreshold)
                    {
                        correspondingSegment = segment;
                        faceDistance = currentDistance;
                    }
                }
                if (correspondingSegment == nullptr)
                {
                    DIFFCHECK_WARN("No segment found for the face. Returning an empty point cloud for this face.");
                    faceSegments.push_back(facePoints);
                    continue;
                }
                bool hasColors = correspondingSegment->GetNumColors() > 0;
                for (Eigen::Vector3d point : correspondingSegment->Points)
                {
                    if (face->IsPointOnFace(point, associationThreshold))
                    {
                        facePoints->Points.push_back(point);
                        facePoints->Normals.push_back(
                            correspondingSegment->Normals[std::distance(
                                correspondingSegment->Points.begin(), 
                                std::find(correspondingSegment->Points.begin(), 
                                correspondingSegment->Points.end(), 
                                point))]
                            );
                        if (hasColors)
                        {
                            facePoints->Colors.push_back(
                                correspondingSegment->Colors[std::distance(
                                    correspondingSegment->Points.begin(), 
                                    std::find(correspondingSegment->Points.begin(), 
                                    correspondingSegment->Points.end(), 
                                    point))]
                                );
                        }
                    }
                }
                for(Eigen::Vector3d point : facePoints->Points)
                {
                    correspondingSegment->Points.erase(
                        std::remove(
                            correspondingSegment->Points.begin(), 
                            correspondingSegment->Points.end(), 
                            point), 
                        correspondingSegment->Points.end());
                }
                if (correspondingSegment->GetNumPoints() == 0)
                {
                    DIFFCHECK_WARN("No point was left in the segment. Deleting the segment.");
                    clusters.erase(
                        std::remove(
                            clusters.begin(), 
                            clusters.end(), 
                            correspondingSegment), 
                        clusters.end());
                }
                faceSegments.push_back(facePoints);
            }
            
        }
        else
        {
            for (std::shared_ptr<diffCheck::geometry::DFMesh> face : referenceMesh)
            {
                std::shared_ptr<geometry::DFPointCloud> correspondingSegment;
                std::shared_ptr<geometry::DFPointCloud> facePoints = std::make_shared<geometry::DFPointCloud>();

                // Getting the center of the mesh
                Eigen::Vector3d faceCenter = face->Cvt2O3DTriangleMesh()->GetCenter();

                // Getting the normal of the mesh face
                Eigen::Vector3d faceNormal = face->GetFirstNormal();
                faceNormal.normalize();
                
                double faceDistance = std::numeric_limits<double>::max();
                if (clusters.size() == 0)
                {
                    DIFFCHECK_WARN("No clusters to associate with the mesh faces. Returning an empty point cloud.");
                    return std::vector<std::shared_ptr<geometry::DFPointCloud>>();
                }
                for (auto segment : clusters)
                {   
                    Eigen::Vector3d segmentNormal = Eigen::Vector3d::Zero();

                    if (segment->GetNumPoints() == 0)
                    {
                        DIFFCHECK_WARN("Empty segment. Skipping the segment.");
                        continue;
                    }
                    Eigen::Vector3d segmentCenter = segment->GetAxixAlignedBoundingBox()[0] + (segment->GetAxixAlignedBoundingBox()[1] - segment->GetAxixAlignedBoundingBox()[0])/2.0;

                    for (auto normal : segment->Normals){segmentNormal += normal;}
                    if (segmentNormal.norm() == 0)
                    {
                        DIFFCHECK_WARN("Segment normal is zero. Skipping the segment.");
                        continue;
                    }
                    segmentNormal.normalize();
                    double currentDitanceOrthogonalToFace = std::abs((faceCenter - segmentCenter).dot(faceNormal));
                    if (std::abs(sin(acos(faceNormal.dot(segmentNormal)))) < angleThreshold 
                        && currentDitanceOrthogonalToFace < maximumFaceSegmentDistance  
                        && currentDitanceOrthogonalToFace < faceDistance)
                    {
                        correspondingSegment = segment;
                        faceDistance = currentDitanceOrthogonalToFace;
                    }
                }

                if (correspondingSegment == nullptr)
                {
                    DIFFCHECK_WARN("No segment found for the face. Returning an empty point cloud for this face.");
                    faceSegments.push_back(facePoints);
                    continue;
                }
                bool hasColors = correspondingSegment->GetNumColors() > 0;

                std::vector<int> indicesToRemove;
                for (size_t i = 0; i < correspondingSegment->Points.size(); i++)
                {
                    const Eigen::Vector3d& point = correspondingSegment->Points[i];

                    if (discriminatePoints)
                    {
                        if (face->IsPointOnFace(point, associationThreshold))
                        {
                            facePoints->Points.push_back(point);
                            facePoints->Normals.push_back(correspondingSegment->Normals[i]);
                            if (hasColors)
                            {
                                facePoints->Colors.push_back(correspondingSegment->Colors[i]);
                            }
                            indicesToRemove.push_back(i);
                        }
                    }
                    else
                    {
                        facePoints->Points.push_back(point);
                        facePoints->Normals.push_back(correspondingSegment->Normals[i]);
                        if (hasColors)
                        {
                            facePoints->Colors.push_back(correspondingSegment->Colors[i]);
                        }
                        indicesToRemove.push_back(i);
                    }
                }
                
                for (auto it = indicesToRemove.rbegin(); it != indicesToRemove.rend(); ++it)
                {
                    int i = *it;

                    correspondingSegment->Points.erase(correspondingSegment->Points.begin() + i);
                    correspondingSegment->Normals.erase(correspondingSegment->Normals.begin() + i);

                    if (hasColors)
                    {
                        correspondingSegment->Colors.erase(correspondingSegment->Colors.begin() + i);
                    }
                }
                faceSegments.push_back(facePoints);
            }
        }
        return faceSegments;
    }

    void DFSegmentation::CleanUnassociatedClusters(
        bool isCylinder,
        bool discriminatePoints,
        std::vector<std::shared_ptr<geometry::DFPointCloud>> &unassociatedClusters,
        std::vector<std::vector<std::shared_ptr<geometry::DFPointCloud>>> &existingPointCloudSegments,
        std::vector<std::vector<std::shared_ptr<geometry::DFMesh>>> meshes,
        double angleThreshold,
        double associationThreshold,
        double maximumFaceSegmentDistance)
    {
        if (unassociatedClusters.size() == 0)
        {
            DIFFCHECK_WARN("No unassociated clusters. Nothing is done");
            return;
        }
        else
        {
            for (std::shared_ptr<geometry::DFPointCloud> cluster : unassociatedClusters)
            {
                std::shared_ptr<geometry::DFMesh> correspondingMeshFace;
                Eigen::Vector3d clusterCenter = Eigen::Vector3d::Zero();
                Eigen::Vector3d clusterNormal = Eigen::Vector3d::Zero();

                if (cluster->GetNumPoints() == 0)
                {
                    DIFFCHECK_WARN("Empty cluster. Skipping the cluster.");
                    continue;
                }
                if (cluster->GetNumNormals() == 0)
                {
                    DIFFCHECK_WARN("Empty normals in the cluster. Skipping the cluster.");
                    continue;
                }
                if (meshes.size() == 0)
                {
                    DIFFCHECK_WARN("No meshes to associate with the clusters. Skipping the cluster.");
                    continue;
                }
                for (const Eigen::Vector3d& point : cluster->Points)
                {
                    clusterCenter += point;
                }
                clusterCenter /= cluster->GetNumPoints();
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
                        if (isCylinder)
                        {
                            std::vector<Eigen::Vector3d> minmax = meshFace->GetTightBoundingBox();
                            Eigen::Vector3d min = minmax[0];
                            Eigen::Vector3d max = minmax[1];

                            std::tuple<Eigen::Vector3d, Eigen::Vector3d> centerAndAxis = mesh[0]->ComputeOBBCenterAndAxis();
                            Eigen::Vector3d center = std::get<0>(centerAndAxis);
                            Eigen::Vector3d axis = std::get<1>(centerAndAxis);
                            double dotProduct = clusterNormal.dot(axis);
                            dotProduct = std::max(-1.0, std::min(1.0, dotProduct));

                            double currentDistance = (center - clusterCenter).norm() ;
                            double adaptedDistance = currentDistance * std::abs(dotProduct);

                            if (std::abs(dotProduct) < angleThreshold 
                                && adaptedDistance < distance 
                                && currentDistance < (max - min).norm()*associationThreshold)
                            {
                                goodMeshIndex = meshIndex;
                                goodFaceIndex = faceIndex;
                                distance = adaptedDistance;
                                correspondingMeshFace = meshFace;
                            }

                        }
                        else
                        {
                            
        
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
                            
                            double anglePenalty = 100*std::abs(clusterNormal.dot(faceNormal));
                            double currentDistance = (clusterCenter - faceCenter).norm() * (.1 + std::abs(dotProduct)) / std::max(anglePenalty, 1.0);
                            double normalAlignment = std::abs(faceNormal.dot(clusterNormal));
                            if (std::abs(std::sqrt(1.0 - normalAlignment * normalAlignment)) < angleThreshold 
                            && currentDistance < maximumFaceSegmentDistance 
                            && currentDistance < distance)
                            {
                                goodMeshIndex = meshIndex;
                                goodFaceIndex = faceIndex;
                                distance = currentDistance;
                                correspondingMeshFace = meshFace;
                            }
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
                if (goodMeshIndex >= existingPointCloudSegments.size() || goodFaceIndex >= existingPointCloudSegments[goodMeshIndex].size())
                {
                    DIFFCHECK_WARN("No segment found for the face. Skipping the face.");
                    continue;
                }
                std::shared_ptr<geometry::DFPointCloud> completed_segment = existingPointCloudSegments[goodMeshIndex][goodFaceIndex];

                std::vector<int> indicesToRemove;
                for (size_t i = 0; i <  cluster->Points.size(); i++)
                {
                    const Eigen::Vector3d& point = cluster->Points[i];
                    if(isCylinder)
                    {
                        completed_segment->Points.push_back(point);
                        completed_segment->Normals.push_back(cluster->Normals[i]);
                        completed_segment->Colors.push_back(cluster->Colors[i]);
                        indicesToRemove.push_back(i);
                    }
                    else
                    {
                        if (discriminatePoints)
                        {
                            if (correspondingMeshFace->IsPointOnFace(point, associationThreshold))
                            {
                                completed_segment->Points.push_back(point);
                                completed_segment->Normals.push_back(cluster->Normals[i]);
                                completed_segment->Colors.push_back(cluster->Colors[i]);
                                indicesToRemove.push_back(i);
                            }
                        }
                        else
                        {
                            completed_segment->Points.push_back(point);
                            completed_segment->Normals.push_back(cluster->Normals[i]);
                            completed_segment->Colors.push_back(cluster->Colors[i]);
                            indicesToRemove.push_back(i);
                        }
                    }
                }
                for (auto it = indicesToRemove.rbegin(); it != indicesToRemove.rend(); ++it) 
                {
                    std::swap(cluster->Points[*it], cluster->Points.back());
                    cluster->Points.pop_back();
                    std::swap(cluster->Normals[*it], cluster->Normals.back());
                    cluster->Normals.pop_back();
                    std::swap(cluster->Colors[*it], cluster->Colors.back());
                    cluster->Colors.pop_back();
                }
            }
        }
    };

} // namespace diffCheck::segmentation