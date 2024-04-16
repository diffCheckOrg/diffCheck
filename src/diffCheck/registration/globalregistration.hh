#pragma once

#include "diffCheck.hh"
#include <open3d/pipelines/registration/Registration.h>
#include <open3d/pipelines/registration/TransformationEstimation.h>

namespace diffCheck::registration
{

class GlobalRegistration
{
    public:

    /** 
    * @brief Compute the "point to point" distance between two point clouds. 
    * 
    * For every point in the source point cloud it looks in the KDTree of the target point cloud and finds the closest point.
    * It returns a vector of distances, one for each point in the source point cloud.
    * 
    * @param source The source diffCheck point cloud
    * @param target The target diffCheck point cloud
    * 
    * @see https://github.com/isl-org/Open3D/blob/main/cpp/open3d/geometry/PointCloud.cpp
    */
    static std::vector<double> ComputeP2PDistance(std::shared_ptr<geometry::DFPointCloud> source, 
                                                  std::shared_ptr<geometry::DFPointCloud> target);
    /**
     * @brief Evaluate the registration of a source point cloud to a target point cloud by applying a transformation matrix to the source point cloud and evaluate the error between the transformed source point cloud and the target point cloud.
     * 
     * @param source The source diffCheck point cloud
     * @param target The target diffCheck point cloud
     * @param transform The vector of transformation matrix to apply to the source point cloud.
    */

    static std::vector<double> EvaluateRegistrations(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                 std::shared_ptr<geometry::DFPointCloud> target,
                                                                 std::vector<Eigen::Matrix<double, 4, 4>> transforms);

    /**
    * @brief Fast Global Registration based on Feature Matching using (Fast) Point Feature Histograms (FPFH) on the source and target point clouds
    *    
    * Very simply, point features are values computed on a point cloud (for example the normal of a point, the curvature, etc.).
    * point features historigrams generalize this concept by computing point features in a local neighborhood of a point, stored as higher-dimentional historigrams.
    * 
    * @note The FPFH hyperspace is dependent on the quality of the surface normal estimations at each point (if pc noisy, historigram different).
    * 
    * @param source the source diffCheck point cloud
    * @param target the target diffCheck point cloud
    * @param voxelSize the size of the voxels used to downsample the point clouds. A higher value will result in a more coarse point cloud (less resulting points).
    * @param radiusKDTreeSearch the radius used to search for neighbors in the KDTree. It is used for the calculation of FPFHFeatures. A higher value will result in heavier computation but potentially more precise.
    * @param maxNeighborKDTreeSearch the maximum number of neighbors to search for in the KDTree. It is used for the calculation of FPFHFeatures. A higher value will result in heavier computation but potentially more precise.
    * @param maxCorrespondenceDistance the maximum distance between correspondences. A higher value will result in more correspondences, but potentially include wrong ones.
    * @param iterationNumber the number of iterations to run the RanSaC registration algorithm. A higher value will take more time to compute but increases the chances of finding a good transformation. As parameter of the FastGlobalRegistrationOption options 
    * @param maxTupleCount the maximum number of tuples to consider in the FPFH hyperspace. A higher value will result in heavier computation but potentially more precise. As parameter of the FastGlobalRegistrationOption options 
    * 
    * @see https://link.springer.com/content/pdf/10.1007/978-3-319-46475-6_47.pdf for the original article on Fast Global Registration
    * @see https://pcl.readthedocs.io/projects/tutorials/en/latest/pfh_estimation.html#pfh-estimation for more information on PFH (from PCL, not Open3D)
    * @see https://mediatum.ub.tum.de/doc/800632/941254.pdf for in-depth documentation on the theory
    */
    static open3d::pipelines::registration::RegistrationResult O3DFastGlobalRegistrationFeatureMatching(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                                                        std::shared_ptr<geometry::DFPointCloud> target,
                                                                                                        bool voxelize = true,
                                                                                                        double voxelSize = 0.01,
                                                                                                        double radiusKDTreeSearch = 3,
                                                                                                        int maxNeighborKDTreeSearch = 50,
                                                                                                        double maxCorrespondenceDistance = 0.05,
                                                                                                        int iterationNumber = 100,
                                                                                                        int maxTupleCount = 500);

    /**
    * @brief Fast Global Registration based on Correspondence using (Fast) Point Feature Histograms (FPFH) on the source and target point clouds. Initially developped in open3d to allow other features then FPFH to be used.
    * 
    * Little information on this registration method compared to Fast Global Registration Feature Matching.
    * If understood correctly, this method finds keypoints in the FPFH hyperspaces of the source and target point clouds and then tries to match them, instead of using all the feature historigrams.
    * 
    * @note The FPFH hyperspace is dependent on the quality of the surface normal estimations at each point (if pc noisy, historigram different).
    * 
    * @param source the source diffCheck point cloud
    * @param target the target diffCheck point cloud
    * @param voxelSize the size of the voxels used to downsample the point clouds. A higher value will result in a more coarse point cloud (less resulting points).
    * @param radiusKDTreeSearch the radius used to search for neighbors in the KDTree. It is used for the calculation of FPFHFeatures
    * @param maxNeighborKDTreeSearch the maximum number of neighbors to search for in the KDTree. It is used for the calculation of FPFHFeatures
    * @param iterationNumber the number of iterations to run the Fast Global Registration algorithm.
    * @param maxTupleCount the maximum number of tuples to consider in the FPFH hyperspace 
    * 
    * @see https://pcl.readthedocs.io/projects/tutorials/en/latest/correspondence_grouping.html (from PCL, not Open3D)
    */ 
    static open3d::pipelines::registration::RegistrationResult O3DFastGlobalRegistrationBasedOnCorrespondence(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                                                              std::shared_ptr<geometry::DFPointCloud> target,
                                                                                                              bool voxelize = true,
                                                                                                              double voxelSize = 0.01,
                                                                                                              double radiusKDTreeSearch = 3,
                                                                                                              int maxNeighborKDTreeSearch = 50,
                                                                                                              double maxCorrespondenceDistance = 0.05,
                                                                                                              int iterationNumber = 100,
                                                                                                              int maxTupleCount = 500);
    /**
    * @brief Ransac registration based on Feature Matching using (Fast) Point Feature Histograms (FPFH) on the source and target point clouds. 
    * 
    * Correspondances are computed between the source and target point clouds FPFH hyperspaces.
    * Then, a transformation is computed that minimizes the error between the correspondances. 
    * If the error is above a certain threshold, the transformation is discarded and a new one is computed.
    * 
    * @note The FPFH hyperspace is dependent on the quality of the surface normal estimations at each point (if pc noisy, historigram different).
    * 
    * @param source the source diffCheck point cloud
    * @param target the target diffCheck point cloud
    * @param voxelSize the size of the voxels used to downsample the point clouds. A higher value will result in a more coarse point cloud (less resulting points).
    * @param radiusKDTreeSearch the radius used to search for neighbors in the KDTree. It is used for the calculation of FPFHFeatures
    * @param maxNeighborKDTreeSearch the maximum number of neighbors to search for in the KDTree. It is used for the calculation of FPFHFeatures
    * @param maxCorrespondenceDistance the maximum distance between correspondences in the FPFH space. A higher value will result in more correspondences, but potentially include wrong ones.
    * @param correspondenceSetSize the number of correspondences to consider in the Ransac algorithm
    */
    static open3d::pipelines::registration::RegistrationResult O3DRansacOnCorrespondence(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                                         std::shared_ptr<geometry::DFPointCloud> target,
                                                                                         bool voxelize = true,
                                                                                         double voxelSize = 0.01,
                                                                                         double radiusKDTreeSearch = 3,
                                                                                         int maxNeighborKDTreeSearch = 50,
                                                                                         double maxCorrespondenceDistance = 0.05,
                                                                                         int ransacN = 3,
                                                                                         double correspondenceCheckerDistance = 0.05,
                                                                                         int ransacMaxIteration = 1000,
                                                                                         double ransacConfidenceThreshold = 0.999);
    /**
    * @brief Ransac registration based on Feature Matching using (Fast) Point Feature Histograms (FPFH) on the source and target point clouds
    * 
    * This method picks random points in the source point cloud, gets the FPFH of those points and find the closest points in the FPFH space of the target point cloud. If the transformation the two sets of point yields a low enough error, it is kept.
    * 
    * @param source the source diffCheck point cloud
    * @param target the target diffCheck point cloud
    * @param voxelSize the size of the voxels used to downsample the point clouds. A higher value will result in a more coarse point cloud (less resulting points).
    * @param radiusKDTreeSearch the radius used to search for neighbors in the KDTree. It is used for the calculation of FPFHFeatures
    * @param maxNeighborKDTreeSearch the maximum number of neighbors to search for in the KDTree. It is used for the calculation of FPFHFeatures
    * @param maxCorrespondenceDistance the maximum distance between correspondences in the FPFH space. A higher value will result in more correspondences, but potentially include wrong ones.
    * @param transformationEstimation the transformation estimation method to use. By default, it uses a point to point transformation estimation.
    * @param ransacN the number of points to sample in the source point cloud. A higher value can result in a more precise transformation, but will take more time to compute.
    * @param correspondenceCheckersDistance the maximum distance between correspondances in the FPFH space before testing a RanSaC model. 
    * 
    * @see https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html#RANSAC (from PCL, not Open3D)
    */
    static open3d::pipelines::registration::RegistrationResult O3DRansacOnFeatureMatching(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                                          std::shared_ptr<geometry::DFPointCloud> target,
                                                                                          bool voxelize = true,
                                                                                          double voxelSize = 0.01,
                                                                                          double radiusKDTreeSearch = 3,
                                                                                          int maxNeighborKDTreeSearch  = 50,
                                                                                          double maxCorrespondenceDistance = 0.05,
                                                                                          open3d::pipelines::registration::TransformationEstimationPointToPoint transformationEstimation = open3d::pipelines::registration::TransformationEstimationPointToPoint(false),
                                                                                          int ransacN = 3,
                                                                                          double correspondenceCheckerDistance = 0.05,
                                                                                          int ransacMaxIteration = 1000,
                                                                                          double ransacConfidenceThreshold = 0.999);

};
}