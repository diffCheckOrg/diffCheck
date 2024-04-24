#pragma once

#include "diffCheck.hh"
#include <open3d/pipelines/registration/Registration.h>
#include <open3d/pipelines/registration/TransformationEstimation.h>

namespace diffCheck::registrations
{
    class DFGlobalRegistrations
    {
    public:  ///< Open3d registrations
        /**
        * @brief Fast Global Registration based on Feature Matching using (Fast) Point Feature Histograms (FPFH) on the source and target point clouds
        *    
        * Very simply, point features are values computed on a point cloud (for example the normal of a point, the curvature, etc.).
        * point features historigrams generalize this concept by computing point features in a local neighborhood of a point, and are stored as 
        * higher-dimentional historigrams. Those historigrams are then used to compute a transformation between the source and target point clouds.
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
        * @return diffCheck::transformation::DFTransformation The result of the registration, containing the transformation matrix and the fitness score.
        * 
        * @see https://www.open3d.org/docs/latest/cpp_api/classopen3d_1_1pipelines_1_1registration_1_1_registration_result.html#a6722256f1f3ddccb2c4ec8d724693974 for more information on the RegistrationResult object
        * @see https://link.springer.com/content/pdf/10.1007/978-3-319-46475-6_47.pdf for the original article on Fast Global Registration
        * @see https://pcl.readthedocs.io/projects/tutorials/en/latest/pfh_estimation.html#pfh-estimation for more information on PFH (from PCL, not Open3D)
        * @see https://mediatum.ub.tum.de/doc/800632/941254.pdf for in-depth documentation on the theory
        */
        static diffCheck::transformation::DFTransformation O3DFastGlobalRegistrationFeatureMatching(
            std::shared_ptr<geometry::DFPointCloud> source, 
            std::shared_ptr<geometry::DFPointCloud> target,
            bool voxelize = true,
            double voxelSize = 0.01,
            double radiusKDTreeSearch = 3,
            int maxNeighborKDTreeSearch = 50,
            double maxCorrespondenceDistance = 0.05,
            int iterationNumber = 100,
            int maxTupleCount = 500);
        /**
        * @brief Ransac registration based on Feature Matching using (Fast) Point Feature Histograms (FPFH) on the source and target point clouds
        * 
        * This method picks random points in the source point cloud, gets the FPFH of those points and find the closest points in the FPFH space of 
        * the target point cloud. If the transformation the two sets of point yields a low enough error, it is kept.
        * 
        * @param source the source diffCheck point cloud
        * @param target the target diffCheck point cloud
        * @param voxelSize the size of the voxels used to downsample the point clouds. A higher value will result in a more coarse point cloud (less resulting points).
        * @param radiusKDTreeSearch the radius used to search for neighbors in the KDTree. It is used for the calculation of FPFHFeatures
        * @param maxNeighborKDTreeSearch the maximum number of neighbors to search for in the KDTree. It is used for the calculation of FPFHFeatures
        * @param maxCorrespondenceDistance the maximum distance between correspondences in the FPFH space. A higher value will result in more correspondences, but potentially include wrong ones.
        * @param isTEstimatePt2Pt the transformation estimation method to use. By default, it uses a point to point transformation estimation. If true it will scale and deform the cloud.
        * @param ransacN the number of points to sample in the source point cloud. A higher value can result in a more precise transformation, but will take more time to compute.
        * @param correspondenceCheckersDistance the maximum distance between correspondances in the FPFH space before testing a RanSaC model. 
        * @return diffCheck::transformation::DFTransformation The result of the registration, containing the transformation matrix and the fitness score.
        * 
        * @see https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html#RANSAC (from PCL, not Open3D)
        */
        static diffCheck::transformation::DFTransformation O3DRansacOnFeatureMatching(
            std::shared_ptr<geometry::DFPointCloud> source,
            std::shared_ptr<geometry::DFPointCloud> target,
            bool voxelize = true,
            double voxelSize = 0.01,
            double radiusKDTreeSearch = 3,
            int maxNeighborKDTreeSearch  = 50,
            double maxCorrespondenceDistance = 0.05,
            bool isTEstimatePt2Pt = false,
            int ransacN = 3,
            double correspondenceCheckerDistance = 0.05,
            int ransacMaxIteration = 1000,
            double ransacConfidenceThreshold = 0.999);

    private: ///< o3d utilities to evaluate registration errors
        /**
         * @brief Evaluate the registration of a source point cloud to a target point cloud by applying a transformation matrix 
         * to the source point cloud and evaluate the error between the transformed source point cloud and the target point cloud.
         * 
         * @param source The source diffCheck point cloud
         * @param target The target diffCheck point cloud
         * @param transform The vector of transformation matrix we want to evaluate. they are applied to the source point cloud.
         * @return std::vector<double> A vector of mean distances, one for each transform.
        */

        static std::vector<double> EvaluateRegistrations(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                    std::shared_ptr<geometry::DFPointCloud> target,
                                                                    std::vector<Eigen::Matrix<double, 4, 4>> transforms);
    };

}