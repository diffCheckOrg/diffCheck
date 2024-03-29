#include "registration.hh"

namespace diffCheck::registration
{
     open3d::pipelines::registration::RegistrationResult Registration::o3dFastGlobalRegistrationFeatureMatching(std::shared_ptr<geometry::DFPointCloud> source, std::shared_ptr<geometry::DFPointCloud> target)
        {
        auto sourceO3d = source->Cvt2O3DPointCloud();
        auto targetO3d = target->Cvt2O3DPointCloud();

        sourceO3d->RandomDownSample(0.1);
        targetO3d->RandomDownSample(0.1);

        std::shared_ptr<open3d::pipelines::registration::Feature> sourceFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*sourceO3d,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(0.25, 30));
        std::shared_ptr<open3d::pipelines::registration::Feature> targetFPFHFeatures = open3d::pipelines::registration::ComputeFPFHFeature(*targetO3d,
                                                                                                                                           open3d::geometry::KDTreeSearchParamHybrid(0.25, 30));
        std::shared_ptr<open3d::pipelines::registration::FastGlobalRegistrationOption> option = std::make_shared<open3d::pipelines::registration::FastGlobalRegistrationOption>();
        option->maximum_correspondence_distance_ = 0.05;
        option->iteration_number_ = 100;
        option->maximum_tuple_count_ = 500;

        auto result = open3d::pipelines::registration::FastGlobalRegistrationBasedOnFeatureMatching(*sourceO3d,
                                                                                                    *targetO3d,
                                                                                                    *sourceFPFHFeatures,
                                                                                                    *targetFPFHFeatures,
                                                                                                    *option);

        return result;
    }
} // namespace diffCheck::registration