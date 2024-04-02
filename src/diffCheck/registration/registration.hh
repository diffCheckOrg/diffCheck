#pragma once

#include "diffCheck.hh"
#include <open3d/pipelines/registration/Registration.h>

namespace diffCheck::registration{

class Registration
{
    public:

    open3d::pipelines::registration::RegistrationResult O3DFastGlobalRegistrationFeatureMatching(std::shared_ptr<geometry::DFPointCloud> source, std::shared_ptr<geometry::DFPointCloud> target);

    open3d::pipelines::registration::RegistrationResult O3DFastGlobalRegistrationBasedOnCorrespondence(std::shared_ptr<geometry::DFPointCloud> source, std::shared_ptr<geometry::DFPointCloud> target);
};
}