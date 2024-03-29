#pragma once

#include "diffCheck.hh"
#include <open3d/pipelines/registration/Registration.h>

namespace diffCheck::registration{

class Registration
{
    public:

    open3d::pipelines::registration::RegistrationResult o3dFastGlobalRegistrationFeatureMatching(std::shared_ptr<geometry::DFPointCloud> source, std::shared_ptr<geometry::DFPointCloud> target);
};
}