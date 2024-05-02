#pragma once
# include "diffCheck.hh"

# include <open3d/pipelines/registration/Registration.h>

namespace diffCheck::registration
{
    class RefinedRegistration
    {
        public: ///< open3d registration methods
        /**
         * @brief Perform ICP registration using Open3D
         * 
         * @param source DFPointCloud source point cloud
         * @param target DFPointCloud Target point cloud
         * @param maxCorrespondenceDistance Maximum relative correspondence distance. 0.01 means 1% of the bounding box diagonal
         * @param scalingForPointToPointTransformationEstimation Enable scaling for point-to-point transformation estimation. by default it is false, to only allow rigid transformations
         * @param maxIteration Maximum number of ICP iterations to use in the p2p transformation estimation
         * @param relativeFitness Threshold for relative fitness to use in the p2p transformation estimation
         * @param relativeRMSE Threshold for relative RMSE to use in the p2p transformation estimation
         * @param usePointToPlane Use point-to-plane ICP instead of point-to-point. This replaces the p2p with the point-to-plane transformation estimation
         * @return diffCheck::transformation::DFTransformation
        */
        static diffCheck::transformation::DFTransformation O3DICP(
            std::shared_ptr<geometry::DFPointCloud> source, 
            std::shared_ptr<geometry::DFPointCloud> target,
            double maxCorrespondenceDistance = 0.01,
            bool scalingForPointToPointTransformationEstimation = false,
            double relativeFitness = 1e-6,
            double relativeRMSE = 1e-6,
            int maxIteration = 30,
            bool usePointToPlane = false);

        /**
         * @brief Perform Generalized ICP registration using Open3D
         * 
         * @param source DFPointCloud source point cloud
         * @param target DFPointCloud Target point cloud
         * @param maxCorrespondenceDistance Maximum relative correspondence distance. 0.01 means 1% of the bounding box diagonal
         * @param maxIteration Maximum number of ICP iterations to use in the p2p transformation estimation
         * @param relativeFitness Threshold for relative fitness to use in the p2p transformation estimation
         * @param relativeRMSE Threshold for relative RMSE to use in the p2p transformation estimation
         * @return diffCheck::transformation::DFTransformation
         */
        static diffCheck::transformation::DFTransformation O3DGeneralizedICP(
            std::shared_ptr<geometry::DFPointCloud> source, 
            std::shared_ptr<geometry::DFPointCloud> target,
            double maxCorrespondenceDistance = 0.01,
            int maxIteration = 30,
            double relativeFitness = 1e-6,
            double relativeRMSE = 1e-6);
    };
}