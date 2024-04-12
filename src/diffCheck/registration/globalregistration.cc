#include "globalRegistration.hh"

namespace diffCheck::registration
{
    std::vector<double> GlobalRegistration::ComputeP2PDistance(std::shared_ptr<geometry::DFPointCloud> source, std::shared_ptr<geometry::DFPointCloud> target)
    {
        std::vector<double> errors;
        auto O3DSourcePointCloud = source->Cvt2O3DPointCloud();
        auto O3DTargetPointCloud = target->Cvt2O3DPointCloud();
        
        std::vector<double> distances;

        distances = O3DSourcePointCloud->ComputePointCloudDistance(*O3DTargetPointCloud);
        return distances;
    }
    open3d::pipelines::registration::RegistrationResult GlobalRegistration::O3DFastGlobalRegistrationFeatureMatching(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                                                                     std::shared_ptr<geometry::DFPointCloud> target,
                                                                                                                     double voxelSize,
                                                                                                                     double radiusKDTreeSearch,
                                                                                                                     int maxNeighborKDTreeSearch,
                                                                                                                     double maxCorrespondenceDistance,
                                                                                                                     int iterationNumber,
                                                                                                                     int maxTupleCount)


        {
        std::shared_ptr<open3d::geometry::PointCloud> sourceO3D = source->Cvt2O3DPointCloud();
        std::shared_ptr<open3d::geometry::PointCloud> targetO3D = target->Cvt2O3DPointCloud();

        sourceO3D->VoxelDownSample(0.01);
        targetO3D->VoxelDownSample(0.01);

        std::shared_ptr<open3d::pipelines::registration::Feature> sourceFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*sourceO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(radiusKDTreeSearch, maxNeighborKDTreeSearch));
        std::shared_ptr<open3d::pipelines::registration::Feature> targetFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*targetO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(radiusKDTreeSearch, maxNeighborKDTreeSearch));
        std::shared_ptr<open3d::pipelines::registration::FastGlobalRegistrationOption> option = std::make_shared<open3d::pipelines::registration::FastGlobalRegistrationOption>();
        option->maximum_correspondence_distance_ = 0.05;
        option->iteration_number_ = 100;
        option->maximum_tuple_count_ = 500;

        auto result = open3d::pipelines::registration::FastGlobalRegistrationBasedOnFeatureMatching(*sourceO3D,
                                                                                                    *targetO3D,
                                                                                                    *sourceFPFHFeatures,
                                                                                                    *targetFPFHFeatures,
                                                                                                    *option);

        return result;
    }

    open3d::pipelines::registration::RegistrationResult GlobalRegistration::O3DFastGlobalRegistrationBasedOnCorrespondence(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                                                                     std::shared_ptr<geometry::DFPointCloud> target,
                                                                                                                     double voxelSize,
                                                                                                                     double radiusKDTreeSearch,
                                                                                                                     int maxNeighborKDTreeSearch,
                                                                                                                     double maxCorrespondenceDistance,
                                                                                                                     int iterationNumber,
                                                                                                                     int maxTupleCount)
    {
        std::shared_ptr<open3d::geometry::PointCloud> sourceO3D = source->Cvt2O3DPointCloud();
        std::shared_ptr<open3d::geometry::PointCloud> targetO3D = target->Cvt2O3DPointCloud();

        sourceO3D->VoxelDownSample(0.01);
        targetO3D->VoxelDownSample(0.01);

        std::shared_ptr<open3d::pipelines::registration::FastGlobalRegistrationOption> option = std::make_shared<open3d::pipelines::registration::FastGlobalRegistrationOption>();
        option->maximum_correspondence_distance_ = 0.05;
        option->iteration_number_ = 100;
        option->maximum_tuple_count_ = 500;

        std::shared_ptr<open3d::pipelines::registration::Feature> sourceFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*sourceO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(radiusKDTreeSearch, maxNeighborKDTreeSearch));
        std::shared_ptr<open3d::pipelines::registration::Feature> targetFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*targetO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(radiusKDTreeSearch, maxNeighborKDTreeSearch));
        

        open3d::pipelines::registration::CorrespondenceSet correspondanceset;
        correspondanceset = open3d::pipelines::registration::CorrespondencesFromFeatures(*sourceFPFHFeatures, *targetFPFHFeatures);

        auto result = open3d::pipelines::registration::FastGlobalRegistrationBasedOnCorrespondence(*sourceO3D,
                                                                                                    *targetO3D,
                                                                                                    correspondanceset,
                                                                                                    *option);
        return result;
    }

    open3d::pipelines::registration::RegistrationResult GlobalRegistration::O3DRansacOnCorrespondence(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                                                                     std::shared_ptr<geometry::DFPointCloud> target,
                                                                                                                     double voxelSize,
                                                                                                                     double radiusKDTreeSearch,
                                                                                                                     int maxNeighborKDTreeSearch,
                                                                                                                     double maxCorrespondenceDistance,
                                                                                                                     int correspondenceSetSize)
    {
        std::shared_ptr<open3d::geometry::PointCloud> sourceO3D = source->Cvt2O3DPointCloud();
        std::shared_ptr<open3d::geometry::PointCloud> targetO3D = target->Cvt2O3DPointCloud();

        sourceO3D->VoxelDownSample(0.01);
        targetO3D->VoxelDownSample(0.01);

        std::shared_ptr<open3d::pipelines::registration::Feature> sourceFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*sourceO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(radiusKDTreeSearch, maxNeighborKDTreeSearch));
        std::shared_ptr<open3d::pipelines::registration::Feature> targetFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*targetO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(radiusKDTreeSearch, maxNeighborKDTreeSearch));
        

        open3d::pipelines::registration::CorrespondenceSet correspondanceset;
        correspondanceset = open3d::pipelines::registration::CorrespondencesFromFeatures(*sourceFPFHFeatures, *targetFPFHFeatures);

        auto result = open3d::pipelines::registration::RegistrationRANSACBasedOnCorrespondence(*sourceO3D,
                                                                                                    *targetO3D,
                                                                                                    correspondanceset,
                                                                                                    maxCorrespondenceDistance, 
                                                                                                    open3d::pipelines::registration::TransformationEstimationPointToPoint(), 
                                                                                                    correspondenceSetSize);
        return result;
    }

    open3d::pipelines::registration::RegistrationResult GlobalRegistration::O3DRansacOnFeatureMatching(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                                                                     std::shared_ptr<geometry::DFPointCloud> target,
                                                                                                                     double voxelSize,
                                                                                                                     double radiusKDTreeSearch,
                                                                                                                     int maxNeighborKDTreeSearch,
                                                                                                                     double maxCorrespondenceDistance)
    {
        std::shared_ptr<open3d::geometry::PointCloud> sourceO3D = source->Cvt2O3DPointCloud();
        std::shared_ptr<open3d::geometry::PointCloud> targetO3D = target->Cvt2O3DPointCloud();

        sourceO3D->VoxelDownSample(0.01);
        targetO3D->VoxelDownSample(0.01);

        std::shared_ptr<open3d::pipelines::registration::Feature> sourceFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*sourceO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(radiusKDTreeSearch, maxNeighborKDTreeSearch));
        std::shared_ptr<open3d::pipelines::registration::Feature> targetFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*targetO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(radiusKDTreeSearch, maxNeighborKDTreeSearch));
        auto result = open3d::pipelines::registration::RegistrationRANSACBasedOnFeatureMatching(*sourceO3D,
                                                                                                    *targetO3D,
                                                                                                    *sourceFPFHFeatures,
                                                                                                    *targetFPFHFeatures,
                                                                                                    false,
                                                                                                    maxCorrespondenceDistance);

        return result;
    }
}