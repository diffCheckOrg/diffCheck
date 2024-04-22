#include "diffCheck/registrations/DFGlobalRegistrations.hh"

namespace diffCheck::registrations
{   
    std::vector<double> DFGlobalRegistrations::EvaluateRegistrations(
        std::shared_ptr<geometry::DFPointCloud> source, 
        std::shared_ptr<geometry::DFPointCloud> target,
        std::vector<Eigen::Matrix<double, 4, 4>> transforms)
    {
        std::vector<double> errors;
        for(int i = 0; i < transforms.size(); i++)
        {
            std::shared_ptr<open3d::geometry::PointCloud> o3DPointCloud = source->Cvt2O3DPointCloud();
            std::shared_ptr<open3d::geometry::PointCloud> o3DPointCloudAfterTrans = std::make_shared<open3d::geometry::PointCloud>(o3DPointCloud->Transform(transforms[i]));
            std::shared_ptr<geometry::DFPointCloud> dfPointCloudPtrAfterTrans = std::make_shared<geometry::DFPointCloud>();
            dfPointCloudPtrAfterTrans->Cvt2DFPointCloud(o3DPointCloudAfterTrans);
            std::vector<double> registrationErrors = dfPointCloudPtrAfterTrans->ComputeP2PDistance(target);
            errors.push_back(std::accumulate(registrationErrors.begin(), registrationErrors.end(), 0.0) / registrationErrors.size());
        }
        return errors;
    };

    diffCheck::transformation::DFTransformation DFGlobalRegistrations::O3DFastGlobalRegistrationFeatureMatching(
        std::shared_ptr<geometry::DFPointCloud> source, 
        std::shared_ptr<geometry::DFPointCloud> target,
        bool voxelise,
        double voxelSize,
        double radiusKDTreeSearch,
        int maxNeighborKDTreeSearch,
        double maxCorrespondenceDistance,
        int iterationNumber,
        int maxTupleCount)
    {
        std::shared_ptr<open3d::geometry::PointCloud> sourceO3D = source->Cvt2O3DPointCloud();
        std::shared_ptr<open3d::geometry::PointCloud> targetO3D = target->Cvt2O3DPointCloud();

        if (voxelise)
        {
            sourceO3D->VoxelDownSample(voxelSize);
            targetO3D->VoxelDownSample(voxelSize);
        }

        std::shared_ptr<open3d::pipelines::registration::Feature> sourceFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*sourceO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(radiusKDTreeSearch, maxNeighborKDTreeSearch));
        std::shared_ptr<open3d::pipelines::registration::Feature> targetFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*targetO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(radiusKDTreeSearch, maxNeighborKDTreeSearch));
        std::shared_ptr<open3d::pipelines::registration::FastGlobalRegistrationOption> option = std::make_shared<open3d::pipelines::registration::FastGlobalRegistrationOption>();
        option->maximum_correspondence_distance_ = maxCorrespondenceDistance;
        option->iteration_number_ = iterationNumber;
        option->maximum_tuple_count_ = maxTupleCount;

        open3d::pipelines::registration::RegistrationResult result = open3d::pipelines::registration::FastGlobalRegistrationBasedOnFeatureMatching(
            *sourceO3D,
            *targetO3D,
            *sourceFPFHFeatures,
            *targetFPFHFeatures,
            *option);
        diffCheck::transformation::DFTransformation transformation = 
            diffCheck::transformation::DFTransformation(result.transformation_);

        return transformation;
    }

    diffCheck::transformation::DFTransformation DFGlobalRegistrations::O3DRansacOnFeatureMatching(
        std::shared_ptr<geometry::DFPointCloud> source, 
        std::shared_ptr<geometry::DFPointCloud> target,
        bool voxelise,
        double voxelSize,
        double radiusKDTreeSearch,
        int maxNeighborKDTreeSearch,
        double maxCorrespondenceDistance,
        open3d::pipelines::registration::TransformationEstimationPointToPoint transformationEstimation,
        int ransacN,
        double correspondenceCheckerDistance ,
        int ransacMaxIteration,
        double ransacConfidenceThreshold)
    {
        std::shared_ptr<open3d::geometry::PointCloud> sourceO3D = source->Cvt2O3DPointCloud();
        std::shared_ptr<open3d::geometry::PointCloud> targetO3D = target->Cvt2O3DPointCloud();

        if (voxelise)
        {
            sourceO3D->VoxelDownSample(voxelSize);
            targetO3D->VoxelDownSample(voxelSize);
        }

        std::shared_ptr<open3d::pipelines::registration::Feature> sourceFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*sourceO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(radiusKDTreeSearch, maxNeighborKDTreeSearch));
        std::shared_ptr<open3d::pipelines::registration::Feature> targetFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*targetO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(radiusKDTreeSearch, maxNeighborKDTreeSearch));
        std::vector<std::reference_wrapper<const open3d::pipelines::registration::CorrespondenceChecker>> correspondanceChecker;
        open3d::pipelines::registration::CorrespondenceCheckerBasedOnDistance checkerOnDistance = open3d::pipelines::registration::CorrespondenceCheckerBasedOnDistance(correspondenceCheckerDistance);
        correspondanceChecker.push_back(checkerOnDistance);
        
        auto result = open3d::pipelines::registration::RegistrationRANSACBasedOnFeatureMatching(*sourceO3D,
                                                                                                    *targetO3D,
                                                                                                    *sourceFPFHFeatures,
                                                                                                    *targetFPFHFeatures,
                                                                                                    false,
                                                                                                    maxCorrespondenceDistance,
                                                                                                    transformationEstimation,
                                                                                                    ransacN,
                                                                                                    correspondanceChecker,
                                                                                                    open3d::pipelines::registration::RANSACConvergenceCriteria(ransacMaxIteration, ransacConfidenceThreshold));

        diffCheck::transformation::DFTransformation transformation = diffCheck::transformation::DFTransformation(result.transformation_);

        return transformation;
    }
}