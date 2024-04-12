#pragma once

#include "diffCheck.hh"
#include <open3d/pipelines/registration/Registration.h>

namespace diffCheck::registration
{

class GlobalRegistration
{
    public:
    
    static std::vector<double> ComputeP2PDistance(std::shared_ptr<geometry::DFPointCloud> source, 
                                                  std::shared_ptr<geometry::DFPointCloud> target);
    
    /**
    Documentation on Fast Point Feature Historigrams: https://pcl.readthedocs.io/projects/tutorials/en/latest/fpfh_estimation.html
    
    Very simply, point features are values computed on a point cloud (for example the normal of a point, the curvature, etc.).
    point features historigrams generalize this concept by computing point features in a local neighborhood of a point, stored as higher-dimentional historigrams.

    For example, for a given point, you take all the neighboring points within a given radius, and create a complete graph on those vertices.
    then for each edge of the graph you compute features that are then stored in a historigram of the original center point from which the sphere and the graph where built.
    https://pcl.readthedocs.io/projects/tutorials/en/latest/pfh_estimation.html#pfh-estimation proposes a simple example of such a historigram.

    PCL's documentation refers to this 2009 TUM PhD thesis (but largely outside the scope of our work): https://mediatum.ub.tum.de/doc/800632/941254.pdf

    Quite important for us: the resultant hyperspace is dependent on the quality of the surface normal estimations at each point (if pc noisy, historigram different).

    @param source the source point cloud
    @param target the target point cloud
    @param voxelSize the size of the voxels used to downsample the point clouds
    @param radiusKDTreeSearch the radius used to search for neighbors in the KDTree. It is used for the calculation of FPFHFeatures
    @param maxNeighborKDTreeSearch the maximum number of neighbors to search for in the KDTree. It is used for the calculation of FPFHFeatures
    @param maxCorrespondenceDistance the maximum distance between correspondences.
    @param iterationNumber the number of iterations to run the RanSaC registration algorithm
    @param maxTupleCount the maximum number of tuples to consider in the FPFH hyperspace
    */
    static open3d::pipelines::registration::RegistrationResult O3DFastGlobalRegistrationFeatureMatching(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                                                        std::shared_ptr<geometry::DFPointCloud> target,
                                                                                                        double voxelSize = 0.01,
                                                                                                        double radiusKDTreeSearch = 3,
                                                                                                        int maxNeighborKDTreeSearch = 50,
                                                                                                        double maxCorrespondenceDistance = 0.05,
                                                                                                        int iterationNumber = 100,
                                                                                                        int maxTupleCount = 500);

    /**
    Little information on this registration method compared to the previous one.
    If I understand correctly, this method finds keypoints in the FPFH hyperspaces of the source and target point clouds and then tries to match them.
    https://pcl.readthedocs.io/projects/tutorials/en/latest/correspondence_grouping.html 

    @param source the source point cloud
    @param target the target point cloud
    @param voxelSize the size of the voxels used to downsample the point clouds
    @param radiusKDTreeSearch the radius used to search for neighbors in the KDTree. It is used for the calculation of FPFHFeatures
    @param maxNeighborKDTreeSearch the maximum number of neighbors to search for in the KDTree. It is used for the calculation of FPFHFeatures
    @param iterationNumber the number of iterations to run the RanSaC registration algorithm
    @param maxTupleCount the maximum number of tuples to consider in the FPFH hyperspace
    */ 
    static open3d::pipelines::registration::RegistrationResult O3DFastGlobalRegistrationBasedOnCorrespondence(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                                                              std::shared_ptr<geometry::DFPointCloud> target,
                                                                                                              double voxelSize = 0.01,
                                                                                                              double radiusKDTreeSearch = 3,
                                                                                                              int maxNeighborKDTreeSearch = 50,
                                                                                                              double maxCorrespondenceDistance = 0.05,
                                                                                                              int iterationNumber = 100,
                                                                                                              int maxTupleCount = 500);
    /**
    Ransac registration based on correspondence:
    Correspondances are computed between the source and target point clouds.
    Then, a transformation is computed that minimizes the error between the correspondances. 
    If the error is above a certain threshold, the transformation is discarded and a new one is computed.

    In practice, Open3D gives little information about the feature correspondence, compared to the FGR methods

    @param source the source point cloud
    @param target the target point cloud
    @param voxelSize the size of the voxels used to downsample the point clouds
    @param radiusKDTreeSearch the radius used to search for neighbors in the KDTree. It is used for the calculation of FPFHFeatures
    @param maxNeighborKDTreeSearch the maximum number of neighbors to search for in the KDTree. It is used for the calculation of FPFHFeatures
    @param maxCorrespondenceDistance the maximum distance between correspondences.
    @param correspondenceSetSize the number of correspondences to consider in the Ransac algorithm

    */
    static open3d::pipelines::registration::RegistrationResult O3DRansacOnCorrespondence(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                                         std::shared_ptr<geometry::DFPointCloud> target,
                                                                                         double voxelSize = 0.01,
                                                                                         double radiusKDTreeSearch = 3,
                                                                                         int maxNeighborKDTreeSearch = 50,
                                                                                         double maxCorrespondenceDistance = 0.05,
                                                                                         int correspondenceSetSize = 200);
    /**
    Ransac registration based on Feature Matching
    https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html#RANSAC

    @param source the source point cloud
    @param target the target point cloud
    @param voxelSize the size of the voxels used to downsample the point clouds
    @param radiusKDTreeSearch the radius used to search for neighbors in the KDTree. It is used for the calculation of FPFHFeatures
    @param maxNeighborKDTreeSearch the maximum number of neighbors to search for in the KDTree. It is used for the calculation of FPFHFeatures
    @param maxCorrespondenceDistance the maximum distance between correspondences.
    */
    static open3d::pipelines::registration::RegistrationResult O3DRansacOnFeatureMatching(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                                          std::shared_ptr<geometry::DFPointCloud> target,
                                                                                          double voxelSize = 0.01,
                                                                                          double radiusKDTreeSearch = 3,
                                                                                          int maxNeighborKDTreeSearch  = 50,
                                                                                          double maxCorrespondenceDistance = 0.05);

};
}