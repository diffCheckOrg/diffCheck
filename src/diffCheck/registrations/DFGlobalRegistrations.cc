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

            std::shared_ptr<open3d::geometry::PointCloud> o3DPointCloudAfterTrans = 
            std::make_shared<open3d::geometry::PointCloud>(o3DPointCloud->Transform(transforms[i]));

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

        // voxelize at the scale of the point cloud
        if (voxelise)
        {
            double absoluteVoxelSize = 
            voxelSize * std::abs(sourceO3D->GetMaxBound().norm() - sourceO3D->GetMinBound().norm());

            sourceO3D->VoxelDownSample(absoluteVoxelSize);
            targetO3D->VoxelDownSample(absoluteVoxelSize);
        }

        if (sourceO3D->normals_.size() == 0)
        {
            sourceO3D->EstimateNormals();
        }

        if (targetO3D->normals_.size() == 0)
        {
            targetO3D->EstimateNormals();
        }

        double absoluteRadiusKDTreeSearch = 
        radiusKDTreeSearch * std::abs(sourceO3D->GetMaxBound().norm() - sourceO3D->GetMinBound().norm());

        std::shared_ptr<open3d::pipelines::registration::Feature> sourceFPFHFeatures = 
        open3d::pipelines::registration::ComputeFPFHFeature(
            *sourceO3D,
            open3d::geometry::KDTreeSearchParamHybrid(absoluteRadiusKDTreeSearch, maxNeighborKDTreeSearch));

        std::shared_ptr<open3d::pipelines::registration::Feature> targetFPFHFeatures =
        open3d::pipelines::registration::ComputeFPFHFeature(
            *targetO3D,
            open3d::geometry::KDTreeSearchParamHybrid(absoluteRadiusKDTreeSearch, maxNeighborKDTreeSearch));

        std::shared_ptr<open3d::pipelines::registration::FastGlobalRegistrationOption> option = 
        std::make_shared<open3d::pipelines::registration::FastGlobalRegistrationOption>();

        option->maximum_correspondence_distance_ = maxCorrespondenceDistance;
        option->iteration_number_ = iterationNumber;
        option->maximum_tuple_count_ = maxTupleCount;

        
        open3d::pipelines::registration::RegistrationResult result = 
        open3d::pipelines::registration::FastGlobalRegistrationBasedOnFeatureMatching(
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
        bool isTEstimatePt2Pt,
        int ransacN,
        double correspondenceCheckerDistance,
        double similarityThreshold,
        int ransacMaxIteration,
        double ransacConfidenceThreshold)
    {
        std::shared_ptr<open3d::geometry::PointCloud> sourceO3D = source->Cvt2O3DPointCloud();
        std::shared_ptr<open3d::geometry::PointCloud> targetO3D = target->Cvt2O3DPointCloud();

        open3d::pipelines::registration::TransformationEstimationPointToPoint transformationEstimation = 
            open3d::pipelines::registration::TransformationEstimationPointToPoint(isTEstimatePt2Pt);

        // voxelize at the scale of the point cloud
        if (voxelise)
        {
            double absoluteVoxelSize = 
            voxelSize * std::abs(sourceO3D->GetMaxBound().norm() - sourceO3D->GetMinBound().norm());

            sourceO3D->VoxelDownSample(absoluteVoxelSize);
            targetO3D->VoxelDownSample(absoluteVoxelSize);
        }
        
        if (sourceO3D->normals_.size() == 0)
        {
            sourceO3D->EstimateNormals();
        }

        if (targetO3D->normals_.size() == 0)
        {
            targetO3D->EstimateNormals();
        }

        // convert the relative values to absolute ones
        double absoluteRadiusKDTreeSearch = 
        radiusKDTreeSearch * std::abs(sourceO3D->GetMaxBound().norm() - sourceO3D->GetMinBound().norm());

        double absoluteCorrespodenceCheckerDistance = 
        correspondenceCheckerDistance * std::abs(sourceO3D->GetMaxBound().norm() - sourceO3D->GetMinBound().norm());

        double absoluteMaxCorrespondenceDistance =
        maxCorrespondenceDistance * std::abs(sourceO3D->GetMaxBound().norm() - sourceO3D->GetMinBound().norm());

        std::shared_ptr<open3d::pipelines::registration::Feature> sourceFPFHFeatures = 
        open3d::pipelines::registration::ComputeFPFHFeature(
            *sourceO3D,
            open3d::geometry::KDTreeSearchParamHybrid(absoluteRadiusKDTreeSearch, maxNeighborKDTreeSearch));

        std::shared_ptr<open3d::pipelines::registration::Feature> targetFPFHFeatures = 
        open3d::pipelines::registration::ComputeFPFHFeature(
            *targetO3D,
            open3d::geometry::KDTreeSearchParamHybrid(absoluteRadiusKDTreeSearch, maxNeighborKDTreeSearch));

        std::vector<std::reference_wrapper<const open3d::pipelines::registration::CorrespondenceChecker>> correspondanceChecker;
        
        open3d::pipelines::registration::CorrespondenceCheckerBasedOnDistance checkerOnDistance = 
        open3d::pipelines::registration::CorrespondenceCheckerBasedOnDistance(absoluteCorrespodenceCheckerDistance);

        open3d::pipelines::registration::CorrespondenceCheckerBasedOnEdgeLength checkerOnEdgeLength = 
        open3d::pipelines::registration::CorrespondenceCheckerBasedOnEdgeLength(similarityThreshold);
        correspondanceChecker.push_back(checkerOnDistance);
        
        
        auto result = open3d::pipelines::registration::RegistrationRANSACBasedOnFeatureMatching(
            *sourceO3D,
            *targetO3D,
            *sourceFPFHFeatures,
            *targetFPFHFeatures,
            true,
            absoluteMaxCorrespondenceDistance,
            transformationEstimation,
            ransacN,
            correspondanceChecker,
            open3d::pipelines::registration::RANSACConvergenceCriteria(ransacMaxIteration, ransacConfidenceThreshold));

        diffCheck::transformation::DFTransformation transformation = diffCheck::transformation::DFTransformation(result.transformation_);

        return transformation;
    }
}