#include "registration.hh"

namespace diffCheck::registration
{
     open3d::pipelines::registration::RegistrationResult Registration::O3DFastGlobalRegistrationFeatureMatching(std::shared_ptr<geometry::DFPointCloud> source, std::shared_ptr<geometry::DFPointCloud> target)
        {
        auto sourceO3D = source->Cvt2O3DPointCloud();
        auto targetO3D = target->Cvt2O3DPointCloud();

        sourceO3D->RandomDownSample(0.1);
        targetO3D->RandomDownSample(0.1);

        std::shared_ptr<open3d::pipelines::registration::Feature> sourceFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*sourceO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(0.25, 30));
        std::shared_ptr<open3d::pipelines::registration::Feature> targetFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*targetO3D,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(0.25, 30));
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
} // namespace diffCheck::registration