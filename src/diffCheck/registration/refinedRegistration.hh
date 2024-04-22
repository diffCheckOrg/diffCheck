#pragma once
# include "diffCheck.hh"

# include <open3d/pipelines/registration/Registration.h>

namespace diffCheck::registration
{
    class RefinedRegistration
    {
        public:
        static open3d::pipelines::registration::RegistrationResult O3DICP(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                          std::shared_ptr<geometry::DFPointCloud> target,
                                                                          double maxCorrespondenceDistance = 0.01);
        static open3d::pipelines::registration::RegistrationResult O3DGeneralizedICP(std::shared_ptr<geometry::DFPointCloud> source, 
                                                                          std::shared_ptr<geometry::DFPointCloud> target,
                                                                          double maxCorrespondenceDistance = 0.01);
    };
}